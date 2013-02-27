# -*- coding: utf-8 -*-

import json

from collections import Sequence
from datetime import datetime

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin  # NOQA

import cosm


DEFAULT_FORMAT = 'json'


class Client(object):

    api_version = 'v2'
    client_class = cosm.Client

    def __init__(self, key):
        self.client = self.client_class(key)
        self.client.base_url += '/{}/'.format(self.api_version)
        self.feeds = FeedsManager(self.client)
        self.triggers = TriggersManager(self.client)


class ManagerBase(object):

    def _url(self, url_or_id):
        url = self.base_url
        if url_or_id:
            url += '/'
            url = urljoin(url, str(url_or_id))
        return url

    def _json_default(self, obj):
        if not isinstance(obj, datetime):
            raise TypeError
        return obj.isoformat() + 'Z'

    def _parse_datetime(self, value):
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")

    def _prepare_params(self, params):
        params = dict(params)
        for name, value in params.items():
            if isinstance(value, datetime):
                params[name] = value.isoformat() + 'Z'
        return params


class FeedsManager(ManagerBase):

    def __init__(self, client):
        self.client = client
        self.base_url = urljoin(client.base_url, 'feeds')

    def create(self, title, **kwargs):
        data = dict(title=title, **kwargs)
        response = self.client.post(self.base_url, data=data)
        response.raise_for_status()
        feed = cosm.Feed(**data)
        feed._manager = self
        feed._data['feed'] = response.headers['location']
        return feed

    def update(self, id_or_url, **kwargs):
        url = self._url(id_or_url)
        response = self.client.put(url, data=kwargs)
        response.raise_for_status()

    def list(self, **params):
        url = self._url(None)
        response = self.client.get(url, params=params)
        response.raise_for_status()
        json = response.json()
        for feed_data in json['results']:
            feed = cosm.Feed(**feed_data)
            feed._manager = self
            yield feed

    def get(self, url_or_id, **params):
        url = self._url(url_or_id)
        params = self._prepare_params(params)
        response = self.client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        datastreams_data = data.pop('datastreams', None)
        feed = cosm.Feed(**data)
        feed._manager = self
        if datastreams_data:
            datastreams = self._coerce_datastreams(
                feed.datastreams, datastreams_data)
            feed._data['datastreams'] = datastreams
        return feed

    def delete(self, url_or_id):
        url = self._url(url_or_id)
        response = self.client.delete(url)
        response.raise_for_status()

    def _coerce_datastreams(self, datastreams_manager, datastreams_data):
        coerce = datastreams_manager._coerce_to_datastream
        datastreams = []
        for data in datastreams_data:
            datastream = coerce(data)
            datastreams.append(datastream)
        return datastreams


class DatastreamsManager(Sequence, ManagerBase):

    def __init__(self, feed):
        self.feed = feed
        feed_manager = getattr(feed, '_manager', None)
        if feed_manager is not None:
            self.client = feed_manager.client
            self.base_url = feed.feed.replace('.json', '') + '/datastreams'
        else:
            self.client = None

    def __contains__(self, value):
        return value in self.datastreams['datastreams']

    def __getitem__(self, item):
        return self._datastreams[item]

    def __len__(self):
        return len(self._datastreams)

    @property
    def _datastreams(self):
        return self.feed._data['datastreams']

    def create(self, id, **kwargs):
        data = {'version': "1.0.0", 'datastreams': [dict(id=id, **kwargs)]}
        response = self.client.post(self.base_url, data=data)
        response.raise_for_status()
        datastream = cosm.Datastream(id=id, **kwargs)
        datastream._manager = self
        return datastream

    def update(self, datastream_id, **kwargs):
        url = self._url(datastream_id)
        response = self.client.put(url, data=kwargs)
        response.raise_for_status()

    def list(self, **params):
        url = self._url('..')
        response = self.client.get(url, params=params)
        response.raise_for_status()
        json = response.json()
        for datastream_data in json.get('datastreams', []):
            datastream = cosm.Datastream(**datastream_data)
            datastream._manager = self
            yield datastream

    def get(self, id, **params):
        url = self._url(id)
        params = self._prepare_params(params)
        response = self.client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        datastream = self._coerce_to_datastream(data)
        return datastream

    def delete(self, url_or_id):
        url = self._url(url_or_id)
        response = self.client.delete(url)
        response.raise_for_status()

    def _coerce_datapoints(self, datapoints_manager, datapoints_data):
        coerce = datapoints_manager._coerce_to_datapoint
        datapoints = []
        for data in datapoints_data:
            data['at'] = self._parse_datetime(data['at'])
            datapoint = coerce(data)
            datapoints.append(datapoint)
        return datapoints

    def _coerce_to_datastream(self, d):
        if isinstance(d, dict):
            datapoints_data = d.pop('datapoints', None)
            datastream = cosm.Datastream(**d)
            if datapoints_data:
                datapoints = self._coerce_datapoints(
                    datastream.datapoints, datapoints_data)
                datastream.datapoints = datapoints
        datastream._manager = self
        return datastream


class DatapointsManager(Sequence, ManagerBase):

    def __init__(self, datastream):
        self.datastream = datastream
        datastream_manager = getattr(datastream, '_manager', None)
        if datastream_manager is not None:
            self.client = datastream._manager.client
            datastream_url = datastream._manager._url(datastream.id)
            self.base_url = datastream_url + '/datapoints'
        else:
            self.client = None

    def __contains__(self, value):
        return value in self.datapoints['datapoints']

    def __getitem__(self, item):
        return self._datapoints[item]

    def __len__(self):
        return len(self._datapoints)

    @property
    def _datapoints(self):
        return self.datastream._data['datapoints']

    def create(self, datapoints):
        datapoints = [self._coerce_to_datapoint(d) for d in datapoints]
        payload = {'datapoints': datapoints}
        response = self.client.post(self.base_url, data=payload)
        response.raise_for_status()
        return datapoints

    def update(self, at, value):
        url = "{}/{}Z".format(self.base_url, at.isoformat())
        payload = {'value': value}
        response = self.client.put(url, data=payload)
        response.raise_for_status()

    def get(self, at):
        url = "{}/{}Z".format(self.base_url, at.isoformat())
        response = self.client.get(url)
        response.raise_for_status()
        data = response.json()
        data['at'] = self._parse_datetime(data['at'])
        return self._coerce_to_datapoint(data)

    def history(self, **params):
        url = self._url('..').rstrip('/')
        params = self._prepare_params(params)
        response = self.client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        for datapoint_data in data['datapoints']:
            datapoint_data['at'] = self._parse_datetime(datapoint_data['at'])
            yield self._coerce_to_datapoint(datapoint_data)

    def delete(self, at=None, **params):
        url = self.base_url
        if at:
            url = "{}/{}Z".format(url, at.isoformat())
        elif params:
            params = self._prepare_params(params)
        response = self.client.delete(url, params=params)
        response.raise_for_status()

    def _coerce_to_datapoint(self, d):
        if isinstance(d, cosm.Datapoint):
            datapoint = self._clone_datapoint(d)
        elif isinstance(d, dict):
            datapoint = cosm.Datapoint(**d)
        datapoint._manager = self
        return datapoint

    def _clone_datapoint(self, d):
        return cosm.Datapoint(**d._data)


class TriggersManager(ManagerBase):

    def __init__(self, client):
        self.client = client
        self.base_url = urljoin(client.base_url, "triggers")

    def create(self, *args, **kwargs):
        trigger = cosm.Trigger(*args, **kwargs)
        response = self.client.post(self.base_url, data=trigger)
        response.raise_for_status()
        trigger._manager = self
        location = response.headers['location']
        trigger._data['id'] = int(location.rsplit('/', 1)[1])
        return trigger

    def get(self, id):
        url = self._url(id)
        response = self.client.get(url)
        response.raise_for_status()
        data = response.json()
        data.pop('id')
        notified_at = data.pop('notified_at', None)
        user = data.pop('user', None)
        trigger = cosm.Trigger(**data)
        trigger._data['id'] = id
        if notified_at:
            trigger._data['notified_at'] = self._parse_datetime(notified_at)
        if user:
            trigger._data['user'] = user
        trigger._manager = self
        return trigger

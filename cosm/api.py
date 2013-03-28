# -*- coding: utf-8 -*-

from collections import Sequence
from datetime import datetime

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin  # NOQA

from cosm.client import Client
from cosm.models import (
    Feed, Datastream, Datapoint, Location, Waypoint, Trigger, Key, Permission,
    Resource)


__all__ = ['CosmAPIClient']


class CosmAPIClient(object):
    """Cosm API client."""

    api_version = 'v2'
    client_class = Client

    def __init__(self, key):
        """Create an instance of an authenticated Cosm API Client."""
        self.client = self.client_class(key)
        self.client.base_url += '/{}/'.format(self.api_version)
        self._feeds = FeedsManager(self.client)
        self._triggers = TriggersManager(self.client)
        self._keys = KeysManager(self.client)

    @property
    def feeds(self):
        """
        Access :class:`.Feed` objects through a :class:`.FeedsManager`.
        """
        return self._feeds

    @property
    def triggers(self):
        """
        Access :class:`.Trigger` objects through a :class:`.TriggersManager`.
        """
        return self._triggers

    @property
    def keys(self):
        """
        Access :class:`.Key` objects through a :class:`.KeysManager`.
        """
        return self._keys


class ManagerBase(object):
    """Abstract base class for all of out manager classes."""

    @property
    def base_url(self):
        if getattr(self, '_base_url', None) is not None:
            return self._base_url
        parent = getattr(self, 'parent', None)
        if parent is None:
            return
        manager = getattr(parent, '_manager', None)
        if manager is None:
            return
        base_url = manager.url(parent.id) + '/' + self.resource
        return base_url

    @base_url.setter  # NOQA
    def base_url(self, base_url):
        self._base_url = base_url

    def url(self, url_or_id=None):
        """Return a url relative to the base url."""
        url = self.base_url
        if url_or_id:
            url = urljoin(url + '/', str(url_or_id))
        return url

    def _parse_datetime(self, value):
        """Parse and return a datetime string from the Cosm API."""
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")

    def _prepare_params(self, params):
        """Prepare parameters to be passed in query strings to the Cosm API."""
        params = dict(params)
        for name, value in params.items():
            if isinstance(value, datetime):
                params[name] = value.isoformat() + 'Z'
        return params


class FeedsManager(ManagerBase):
    """Create, update and return Feed objects.

    This manager should live on a :class:`.CosmAPIClient` instance and not
    instantiated directly.

    """

    resource = 'feeds'

    def __init__(self, client):
        self.client = client
        self.base_url = client.base_url + self.resource

    def create(self, title, **kwargs):
        """Create a new Feed."""
        data = dict(title=title, version=Feed.VERSION, **kwargs)
        response = self.client.post(self.url(), data=data)
        response.raise_for_status()
        location = response.headers['location']
        feed.feed = location
        feed.id = _id_from_url(location)
        return feed

    def update(self, id_or_url, **kwargs):
        """Update an existing feed by its id or url."""
        url = self.url(id_or_url)
        response = self.client.put(url, data=kwargs)
        response.raise_for_status()

    def list(self, **params):
        """Return a list of feeds."""
        url = self.url()
        response = self.client.get(url, params=params)
        response.raise_for_status()
        json = response.json()
        for feed_data in json['results']:
            feed = self._coerce_feed(feed_data)
            yield feed

    def get(self, url_or_id, **params):
        """Fetch a feed by id or url."""
        url = self.url(url_or_id)
        params = self._prepare_params(params)
        response = self.client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        feed = self._coerce_feed(data)
        return feed

    def delete(self, url_or_id):
        """Delete a feed by id or url."""
        url = self.url(url_or_id)
        response = self.client.delete(url)
        response.raise_for_status()

    def _coerce_feed(self, feed_data):
        datastreams_data = feed_data.pop('datastreams', None)
        location_data = feed_data.pop('location', None)
        feed = Feed(**feed_data)
        feed._manager = self
        if datastreams_data:
            datastreams_manager = DatastreamsManager(feed)
            datastreams = self._coerce_datastreams(
                datastreams_data, datastreams_manager)
            feed._data['datastreams'] = datastreams
            feed._datastreams = datastreams_manager
        if location_data:
            feed._data['location'] = self._coerce_location(location_data)
        return feed

    def _coerce_datastreams(self, datastreams_data, datastreams_manager):
        datastreams = []
        for data in datastreams_data:
            datastream = datastreams_manager._coerce_datastream(data)
            datastreams.append(datastream)
        return datastreams

    def _coerce_location(self, instance):
        if isinstance(instance, Location):
            location = instance
        else:
            location_data = dict(**instance)
            waypoints_data = location_data.pop('waypoints', None)
            if waypoints_data is not None:
                waypoints = self._coerce_waypoints(waypoints_data)
                location_data['waypoints'] = waypoints
            location = Location(**location_data)
        return location

    def _coerce_waypoints(self, waypoints_data):
        waypoints = []
        for data in waypoints_data:
            at = self._parse_datetime(data['at'])
            data = {k: v for k, v in data.items() if k != 'at'}
            waypoint = Waypoint(at=at, **data)
            waypoints.append(waypoint)
        return waypoints


class DatastreamsManager(Sequence, ManagerBase):
    """Create, update and return Datastream objects.

    Instances of this class hang off of :class:`.Feed` objects to manage
    datastreams of that feed.

    A list of datastreams can be retrieved along with the feed which can be
    accessed via this instance as a sequence.

    """

    resource = 'datastreams'

    def __init__(self, feed):
        self.parent = feed
        feed_manager = getattr(feed, '_manager', None)
        self.client = getattr(feed_manager, 'client', None)

    def __contains__(self, value):
        return value in self.datastreams['datastreams']

    def __getitem__(self, item):
        return self._datastreams[item]

    def __len__(self):
        return len(self._datastreams)

    @property
    def _datastreams(self):
        return self.parent._data.setdefault('datastreams', [])

    def create(self, id, **kwargs):
        """Create a new datastream on a feed."""
        data = {
            'version': self.parent.version,
            'datastreams': [dict(id=id, **kwargs)],
        }
        response = self.client.post(self.url(), data=data)
        response.raise_for_status()
        datastream = Datastream(id=id, **kwargs)
        datastream._manager = self
        return datastream

    def update(self, datastream_id, **kwargs):
        """Update a feeds datastream by id."""
        url = self.url(datastream_id)
        response = self.client.put(url, data=kwargs)
        response.raise_for_status()

    def list(self, **params):
        """Return a list of datastreams for the parent feed object."""
        url = self.url('..')
        response = self.client.get(url, params=params)
        response.raise_for_status()
        json = response.json()
        for datastream_data in json.get('datastreams', []):
            datastream = Datastream(**datastream_data)
            datastream._manager = self
            yield datastream

    def get(self, id, **params):
        """Fetch and return a feeds datastream by its id."""
        url = self.url(id)
        params = self._prepare_params(params)
        response = self.client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        datastream = self._coerce_datastream(data)
        return datastream

    def delete(self, url_or_id):
        """Delete a datastream by id or url."""
        url = self.url(url_or_id)
        response = self.client.delete(url)
        response.raise_for_status()

    def _coerce_datapoints(self, datapoints_manager, datapoints_data):
        datapoints = []
        for data in datapoints_data:
            data['at'] = self._parse_datetime(data['at'])
            datapoint = datapoints_manager._coerce_datapoint(data)
            datapoints.append(datapoint)
        return datapoints

    def _coerce_datastream(self, d):
        if isinstance(d, dict):
            datapoints_data = d.pop('datapoints', None)
            datastream = Datastream(**d)
            if datapoints_data:
                datapoints = self._coerce_datapoints(
                    datastream.datapoints, datapoints_data)
                datastream.datapoints = datapoints
        elif isinstance(d, Datastream):
            datastream = d
        datastream._manager = self
        return datastream


class DatapointsManager(Sequence, ManagerBase):
    """Manage datapoints of a datastream.

    A list of :class:`.Datapoint` objects can be retrieved along with the
    :class:`.Datastream` (or :class:`.Feed`) which can be accessed via this
    instance as a sequence.

    """

    resource = 'datapoints'

    def __init__(self, datastream):
        self.parent = datastream
        datastream_manager = getattr(datastream, '_manager', None)
        self.client = getattr(datastream_manager, 'client', None)

    def __contains__(self, value):
        return value in self.datapoints['datapoints']

    def __getitem__(self, item):
        return self._datapoints[item]

    def __len__(self):
        return len(self._datapoints)

    @property
    def _datapoints(self):
        return self.parent._data['datapoints']

    def create(self, datapoints):
        """Create a number of new datapoints for this datastream."""
        datapoints = [self._coerce_datapoint(d) for d in datapoints]
        payload = {'datapoints': datapoints}
        response = self.client.post(self.url(), data=payload)
        response.raise_for_status()
        return datapoints

    def update(self, at, value):
        """Update the value of a datapiont at a given timestamp."""
        url = "{}/{}Z".format(self.url(), at.isoformat())
        payload = {'value': value}
        response = self.client.put(url, data=payload)
        response.raise_for_status()

    def get(self, at):
        """Fetch and return a :class:`.Datapoint` at the given timestamp."""
        url = "{}/{}Z".format(self.url(), at.isoformat())
        response = self.client.get(url)
        response.raise_for_status()
        data = response.json()
        data['at'] = self._parse_datetime(data['at'])
        return self._coerce_datapoint(data)

    def history(self, **params):
        """Fetch and return a list of datapoints in a given timerange."""
        url = self.url('..').rstrip('/')
        params = self._prepare_params(params)
        response = self.client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        for datapoint_data in data.get('datapoints', []):
            datapoint_data['at'] = self._parse_datetime(datapoint_data['at'])
            yield self._coerce_datapoint(datapoint_data)

    def delete(self, at=None, **params):
        """Delete a datapoint or a range of datapoints."""
        url = self.url()
        if at:
            url = "{}/{}Z".format(url, at.isoformat())
        elif params:
            params = self._prepare_params(params)
        response = self.client.delete(url, params=params)
        response.raise_for_status()

    def _coerce_datapoint(self, d):
        if isinstance(d, Datapoint):
            datapoint = self._clone_datapoint(d)
        elif isinstance(d, dict):
            datapoint = Datapoint(**d)
        datapoint._manager = self
        return datapoint

    def _clone_datapoint(self, d):
        return Datapoint(**d._data)


class TriggersManager(ManagerBase):
    """Manage :class:`.Trigger`.

    This manager should live on a :class:`.CosmAPIClient` instance and not
    instantiated directly.

    """

    resource = 'triggers'

    def __init__(self, client):
        self.client = client
        self.base_url = client.base_url + self.resource

    def create(self, *args, **kwargs):
        """Create a new :class:`.Trigger`.

        :returns: A new :class:`.Trigger` object.

        """
        trigger = Trigger(*args, **kwargs)
        response = self.client.post(self.url(), data=trigger)
        response.raise_for_status()
        trigger._manager = self
        location = response.headers['location']
        trigger._data['id'] = int(location.rsplit('/', 1)[1])
        return trigger

    def get(self, id):
        """Fetch and return an existing trigger by its id."""
        url = self.url(id)
        response = self.client.get(url)
        response.raise_for_status()
        data = response.json()
        data.pop('id')
        notified_at = data.pop('notified_at', None)
        user = data.pop('user', None)
        trigger = Trigger(**data)
        trigger._data['id'] = id
        if notified_at:
            trigger._data['notified_at'] = self._parse_datetime(notified_at)
        if user:
            trigger._data['user'] = user
        trigger._manager = self
        return trigger

    def update(self, id, **kwargs):
        """Update an existing trigger."""
        url = self.url(id)
        response = self.client.put(url, data=kwargs)
        response.raise_for_status()

    def list(self, **params):
        """Return a list of triggers."""
        url = self.url()
        response = self.client.get(url, params=params)
        response.raise_for_status()
        json = response.json()
        for data in json:
            trigger = Trigger(**data)
            trigger._manager = self
            yield trigger

    def delete(self, url_or_id):
        """Delete a trigger by id or url."""
        url = self.url(url_or_id)
        response = self.client.delete(url)
        response.raise_for_status()


class KeysManager(ManagerBase):
    """Manage keys their permissions and restrict by resource."""

    resource = 'keys'

    def __init__(self, client):
        self.client = client
        self.base_url = client.base_url + self.resource

    def create(self, label, permissions, **kwargs):
        """Create a new API key."""
        data = dict(label=label, permissions=permissions, **kwargs)
        response = self.client.post(self.url(), data={'key': data})
        response.raise_for_status()
        location = response.headers['Location']
        data['api_key'] = _id_from_url(location)
        key = self._coerce_key(data)
        return key

    def list(self, feed_id=None, **kwargs):
        """List all API keys for this account or for the given feed."""
        url = self.url()
        params = {}
        if feed_id is not None:
            params['feed_id'] = feed_id
        params.update(kwargs)
        response = self.client.get(url, params=params)
        response.raise_for_status()
        json = response.json()
        for data in json['keys']:
            key = self._coerce_key(data)
            yield key

    def get(self, key_id, **params):
        """Fetch and return an API key by its id."""
        url = self.url(key_id)
        response = self.client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        key = self._coerce_key(data['key'])
        return key

    def delete(self, key_id):
        """Delete an API key."""
        url = self.url(key_id)
        response = self.client.delete(url)
        response.raise_for_status()

    def _coerce_key(self, data):
        api_key = data.get('api_key')
        permissions_data = data.get('permissions', [])
        data = {k: v for (k, v) in data.items() if k != 'api_key'}
        permissions = []
        for permission_data in permissions_data:
            permission = self._coerce_permission(permission_data)
            permissions.append(permission)
        data['permissions'] = permissions
        key = Key(**data)
        key._data['api_key'] = api_key
        key._manager = self
        return key

    def _coerce_permission(self, data):
        if isinstance(data, Permission):
            return data
        resources_data = data.get('resources')
        data = {k: v for (k, v) in data.items() if k != 'resources'}
        permission = Permission(**data)
        if resources_data:
            resources = []
            for resource_data in resources_data:
                resource = self._coerce_resource(resource_data)
                resources.append(resource)
            permission._data['resources'] = resources
        return permission

    def _coerce_resource(self, data):
        resource = Resource(**data)
        return resource


def _id_from_url(url):
    """Return the last part or a url

    >>> _id_from_url('http://api.cosm.com/v2/feeds/1234')
    '1234'

    """
    id = url.rsplit('/', 1)[1]
    return id

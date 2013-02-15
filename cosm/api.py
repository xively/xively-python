# -*- coding: utf-8 -*-

import json
import re
import xml.etree.cElementTree as ET

from urlparse import urljoin

import cosm


DEFAULT_FORMAT = 'json'


class Client(object):

    api_version = 'v2'

    def __init__(self, key):
        self.client = cosm.Client(key)
        self.client.base_url += '/{}/'.format(self.api_version)
        self.feeds = FeedsManager(self)


class RESTBase(object):

    _ext_re = re.compile('(.+)(\.[^.]+)?$')
    _parsers = {
        'json': lambda r: r.json(),
        'xml': lambda r: ET.parsestring(r.content),
        'png': lambda r: r.content,
    }

    def _replace_ext(self, url, ext):
        return self._ext_re.sub(r'\1.' + ext, url)

    def _url(self, url_or_id, format=None):
        url = self.base_url
        if url_or_id:
            url += '/'
            url = urljoin(url, str(url_or_id))
        if format:
            url = self._replace_ext(url, format)
        return url


class ManagerMapper(object):

    def __init__(self, manager_class, api, base_url):
        self.manager_class = manager_class
        self.api = api
        self.base_url = base_url

    def __getitem__(self, key):
        url = urljoin(self.base_url + '/', str(key))
        return self.manager_class(self.api, url)


class FeedsManager(RESTBase):

    def __init__(self, api):
        self.api = api
        self.base_url = api.client.base_url + 'feeds'

    @property
    def datastreams(self):
        datastreams = getattr(self, '_datastreams', None)
        if datastreams is None:
            self._datastreams = ManagerMapper(
                DatastreamsManager, self.api, self.base_url)
        return self._datastreams

    def create(self, title, **kwargs):
        payload = dict(title=title, **kwargs)
        response = self.api.client.post(self.base_url, data=payload)
        response.raise_for_status()
        return response.headers['location']

    def update(self, url_or_id, **kwargs):
        url = self._url(url_or_id)
        payload = json.dumps(kwargs)
        response = self.api.client.put(url, data=payload)
        response.raise_for_status()

    def list(self, format=DEFAULT_FORMAT, **params):
        url = self._url(None, format)
        response = self.api.client.get(url, params=params)
        response.raise_for_status()
        return self._parsers[format](response)

    def get(self, url_or_id, format=DEFAULT_FORMAT, **params):
        url = self._url(url_or_id, format)
        response = self.api.client.get(url, **params)
        response.raise_for_status()
        return self._parsers[format](response)

    def delete(self, url_or_id):
        url = self._url(url_or_id)
        response = self.api.client.delete(url)
        response.raise_for_status()


class DatastreamsManager(RESTBase):

    def __init__(self, api, base_url=None):
        self.api = api
        self.base_url = base_url + '/datastreams'

    @property
    def datapoints(self):
        datapoints = getattr(self, '_datapoints', None)
        if datapoints is None:
            self._datapoints = ManagerMapper(
                DatapointsManager, self.api, self.base_url)
        return self._datapoints

    def create(self, id, **kwargs):
        payload = dict(id=id, **kwargs)
        response = self.api.client.post(self.base_url, data=payload)
        response.raise_for_status()

    def update(self, url_or_id, **kwargs):
        url = self._url(url_or_id)
        payload = json.dumps(kwargs)
        response = self.api.client.put(url, data=payload)
        response.raise_for_status()

    def list(self, format=DEFAULT_FORMAT, **params):
        url = self._url(None, format)
        response = self.api.client.get(url, params=params)
        response.raise_for_status()
        return self._parsers[format](response)

    def get(self, url_or_id, format=DEFAULT_FORMAT, **params):
        url = self._url(url_or_id, format)
        response = self.api.client.get(url, **params)
        response.raise_for_status()
        return self._parsers[format](response)

    def delete(self, url_or_id):
        url = self._url(url_or_id)
        response = self.api.client.delete(url)
        response.raise_for_status()


class DatapointsManager(RESTBase):

    def __init__(self, api, base_url=None):
        self.api = api
        self.base_url = base_url + '/datapoints'

    def create(self, datapoints):
        payload = json.dumps(datapoints)
        response = self.api.client.post(self.base_url, data=payload)
        response.raise_for_status()

    def update(self, at, value):
        url = self._url(at)
        payload = json.dumps({'value': value})
        response = self.api.client.put(url, data=payload)
        response.raise_for_status()

    def get(self, at, format=DEFAULT_FORMAT):
        url = self._url(at, format)
        response = self.api.client.get(url)
        response.raise_for_status()
        return self._parsers[format](response)

    def delete(self, at):
        url = self._url(at)
        response = self.api.client.delete(url)
        response.raise_for_status()

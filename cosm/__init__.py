# -*- coding: utf-8 -*-

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

from requests.sessions import Session

from requests.auth import AuthBase


class KeyAuth(AuthBase):
    """Attaches HTTP API Key Authentication to the given Request object."""
    def __init__(self, key):
        self.key = key

    def __call__(self, r):
        # modify and return the request
        r.headers['X-ApiKey'] = self.key
        return r


class Client(Session):
    """A Cosm API Client object.

    This is instantiated with an API key which is used for all requests to the
    Cosm API.  It also defines a BASE_URL so that we can specify relative urls
    when using the client (all requests via this client are going to Cosm).

    """
    BASE_URL = "http://api.cosm.com"

    def __init__(self, key):
        super(Client, self).__init__()
        self.auth = KeyAuth(key)
        self.base_url = self.BASE_URL

    def request(self, method, url, *args, **kwargs):
        """Constructs and sends a Request to the Cosm API.

        Objects that implement __getstate__  will be serialised.

        """
        full_url = urljoin(self.base_url, url)
        if 'data' in kwargs and hasattr(kwargs['data'], '__getstate__'):
            kwargs['data'] = kwargs['data'].__getstate__()
        return super(Client, self).request(method, full_url, *args, **kwargs)


class Base(object):
    """Abstract base class to store API data and allow (de)serialisation."""

    def __init__(self):
        self._data = {}

    def __getstate__(self):
        return self._data

    def __getattr__(self, name):
        return self._data[name]

    def __setattr__(self, name, value):
        if not name.startswith('_'):
            self._data[name] = value
        else:
            super(Base, self).__setattr__(name, value)


class Feed(Base):
    """Cosm Feed, which can contain a number of Datastreams."""

    _datastreams = None

    def __init__(self, title, **kwargs):
        super(Feed, self).__init__()
        self._data['title'] = title
        self._data.update(kwargs)

    @property
    def datastreams(self):
        if self._datastreams is None:
            import cosm.api
            self._datastreams = cosm.api.DatastreamsManager(
                self._manager.client, self.feed)
        return self._datastreams

    def update(self):
        self._manager.update(self.feed, **self.__getstate__())

    def delete(self):
        self._manager.delete(self.feed)


class Datastream(Base):
    """Cosm Datastream containing current and historical values."""

    def __init__(self, id, **kwargs):
        super(Datastream, self).__init__()
        self._data['id'] = id
        self._data.update(**kwargs)


class Datapoint(Base):
    """A Datapoint represents a value at a certain point in time."""

    def __init__(self, at, value):
        super(Datapoint, self).__init__()
        self._data['at'] = at
        self._data['value'] = value

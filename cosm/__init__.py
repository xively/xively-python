# -*- coding: utf-8 -*-

from urlparse import urljoin
from requests.sessions import Session


class Client(Session):
    """A Cosm API Client object.

    This is instantiated with an API key which is used for all requests to the
    Cosm API.  It also defines a BASE_URL so that we can specify relative urls
    when using the client (all requests via this client are going to Cosm).

    """
    BASE_URL = "http://api.cosm.com"

    def __init__(self, key):
        self.key = key
        super(Client, self).__init__()

    def request(self, method, url, *args, **kwargs):
        """Constructs and sends a Request to the Cosm API.

        Objects that implement __getstate__  will be serialised.

        """
        full_url = urljoin(self.BASE_URL, url)
        if 'data' in kwargs and hasattr(kwargs['data'], '__getstate__'):
            kwargs['data'] = kwargs['data'].__getstate__()
        return super(Client, self).request(method, full_url, *args, **kwargs)


class Base(object):
    """Abstract base class to store API data and allow (de)serialisation."""

    def __init__(self):
        self._data = {}

    def __getstate__(self):
        return self._data

    def __setstate__(self, state):
        self._data.clear()
        self._data.update(state)


class Feed(Base):
    """Cosm Feed, which can contain a number of Datastreams."""

    def __init__(self, title):
        super(Feed, self).__init__()
        self._data['title'] = title


class Datastream(Base):
    """Cosm Datastream containing current and historical values."""

    def __init__(self, id):
        super(Datastream, self).__init__()
        self._data['id'] = id


class Datapoint(Base):
    """A Datapoint represents a value at a certain point in time."""

    def __init__(self, at, value):
        super(Datapoint, self).__init__()
        self._data['at'] = at
        self._data['value'] = value

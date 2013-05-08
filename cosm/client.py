# -*- coding: utf-8 -*-

import json

from datetime import datetime

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin  # NOQA

from requests.auth import AuthBase
from requests.sessions import Session

import cosm


__all__ = ['Client']


class KeyAuth(AuthBase):
    """Attaches HTTP API Key Authentication to the given Request object."""
    def __init__(self, key):
        self.key = key

    def __call__(self, r):
        # modify and return the request
        r.headers['X-ApiKey'] = self.key
        return r


class Client(Session):
    r"""A Cosm API Client object.

    This is instantiated with an API key which is used for all requests to the
    Cosm API.  It also defines a BASE_URL so that we can specify relative urls
    when using the client (all requests via this client are going to Cosm).

    :param key: A Cosm API Key
    :type key: str
    :param use_ssl: Use https for all connections instead of http
    :type use_ssl: bool [False]
    :param verify: Verify SSL certificates (default: True)

    A Client instance can also be used when you want low level access to the
    API and can be used with CSV or XML instead of the default JSON.

    Usage::

        >>> client = cosm.Client("YOUR_API_KEY")
        >>> body = "1,123\r\n2,456\r\n"
        >>> client.post('/v2/feeds/1977.csv', data=body)
        <Response [200]>

    """
    BASE_URL = "//api.cosm.com"

    def __init__(self, key, use_ssl=False, verify=True):
        super(Client, self).__init__()
        self.auth = KeyAuth(key)
        self.base_url = ('https:' if use_ssl else 'http:') + self.BASE_URL
        self.headers['Content-Type'] = 'application/json'
        self.headers['User-Agent'] = 'cosm-python/{} {}'.format(
            cosm.__version__, self.headers['User-Agent'])
        self._json_encoder = JSONEncoder()
        self.verify = verify

    def request(self, method, url, *args, **kwargs):
        """Constructs and sends a Request to the Cosm API.

        Objects that implement __getstate__  will be serialised.

        """
        full_url = urljoin(self.base_url, url)
        if 'data' in kwargs:
            kwargs['data'] = self._encode_data(kwargs['data'])
        return super(Client, self).request(method, full_url, *args, **kwargs)

    def _encode_data(self, data, **kwargs):
        """Returns data encoded as JSON using a custom encoder.

        >>> import cosm
        >>> client = Client("API_KEY")
        >>> client._encode_data({'foo': datetime(2013, 2, 22, 12, 14, 40)})
        '{"foo": "2013-02-22T12:14:40Z"}'
        >>> feed = cosm.Feed(title="The Answer")
        >>> client._encode_data({'feed': feed}, sort_keys=True)
        '{"feed": {"title": "The Answer", "version": "1.0.0"}}'
        >>> datastreams = [cosm.Datastream(id="1"), cosm.Datastream(id="2")]
        >>> client._encode_data({'datastreams': datastreams})
        '{"datastreams": [{"id": "1"}, {"id": "2"}]}'
        """
        encoder = JSONEncoder(**kwargs) if kwargs else self._json_encoder
        return encoder.encode(data)


class JSONEncoder(json.JSONEncoder):
    """Encoder that can handle datetime objects or cosm models."""

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat() + 'Z'
        elif hasattr(obj, '__getstate__'):
            return obj.__getstate__()
        else:
            return json.JSONEncoder.default(self, obj)

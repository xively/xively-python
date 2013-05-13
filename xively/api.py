# -*- coding: utf-8 -*-

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin  # NOQA

from xively.client import Client
from xively.managers import FeedsManager, KeysManager, TriggersManager


__all__ = ['XivelyAPIClient']


class XivelyAPIClient(object):
    """An instance of an authenticated Xively API Client.

    The root object from which the user can manage feeds, keys and triggers.

    :param key: A Xively API Key
    :type key: str
    :param use_ssl: Use https for all connections instead of http
    :type use_ssl: bool [False]
    :param kwargs: Other additional keyword arguments to pass to client

    Usage::

        >>> import xively
        >>> xively.XivelyAPIClient("API_KEY")
        <xively.XivelyAPIClient()>

        >>> api = xively.XivelyAPIClient("API_KEY", use_ssl=True)
        >>> api.feeds.base_url
        'https://api.xively.com/v2/feeds'
        >>> api.triggers.base_url
        'https://api.xively.com/v2/triggers'
        >>> api.keys.base_url
        'https://api.xively.com/v2/keys'

    """
    api_version = 'v2'
    client_class = Client

    def __init__(self, key, use_ssl=False, **kwargs):
        self.client = self.client_class(key, use_ssl=use_ssl, **kwargs)
        self.client.base_url += '/{}/'.format(self.api_version)
        self._feeds = FeedsManager(self.client)
        self._triggers = TriggersManager(self.client)
        self._keys = KeysManager(self.client)

    def __repr__(self):
        return "<{}.{}()>".format(__package__, self.__class__.__name__)

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

# -*- coding: utf-8 -*-

__title__ = 'cosm-python'
__version__ = '0.1.0'

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin  # NOQA


__all__ = ['Feed', 'Datastream', 'Datapoint', 'Location', 'Waypoint',
           'Trigger', 'Key', 'Permission', 'Resource']


class Base(object):
    """Abstract base class to store API data and allow (de)serialisation."""

    def __init__(self):
        self._data = {}

    def __getstate__(self):
        """Returns the current state of the object.

        This is the data that should be sent to the Cosm API.
        """
        return {k: v for k, v in self._data.items() if v is not None}

    def __getattr__(self, name):
        """Looks up and returns an attribute from the state."""
        try:
            return self._data[name]
        except KeyError:
            class_name = self.__class__.__name__
            raise AttributeError(
                "'{}' object has no attribute '{}'".format(class_name, name))

    def __setattr__(self, name, value):
        """Sets the value of an attribute in the state."""
        if not name.startswith('_') and name not in dir(self.__class__):
            self._data[name] = value
        else:
            super(Base, self).__setattr__(name, value)


class Feed(Base):
    """Cosm Feed, which can contain a number of Datastreams.

    :param title: A descriptive name for the feed
    :param website: The URL of a website which is relevant to this feed e.g.
        home page
    :param tags: Tagged metadata about the environment (characters ' " and
        commas will be stripped out)
    :param location: :class:`.Location` object for this feed
    :param private: Whether the environment is private or not.
    :type private: bool

    Usage::

        >>> import cosm
        >>> cosm.Feed(title="Cosm Office environment")
        <cosm.Feed(None)>

    """

    VERSION = "1.0.0"

    _datastreams = None

    def __init__(self, title, **kwargs):
        self._data = {
            'title': title,
            'version': self.VERSION,
        }
        if 'datastreams' in kwargs:
            self.datastreams = kwargs.pop('datastreams')
        self._data.update(kwargs)

    def __repr__(self):
        return "<{}.{}({id})>".format(
            __package__, self.__class__.__name__, id=self._data.get('id'))

    @property
    def datastreams(self):
        """Manager for datastreams of this feed.

        When fetched from the API, datastreams behaves liek a cache, populated
        with the most recently updated datastreams for this feed. The manager
        can also be used to create, update and delete datastreams for this
        feed.

        Usage::

            >>> import cosm
            >>> api = cosm.CosmAPIClient("API_KEY")
            >>> feed = api.feeds.get(7021)
            >>> feed.datastreams[0]  # doctest: +IGNORE_UNICODE
            <cosm.Datastream('3')>

        """
        if self._datastreams is None:
            import cosm.api
            self._datastreams = cosm.api.DatastreamsManager(self)
        return self._datastreams

    @datastreams.setter  # NOQA
    def datastreams(self, datastreams):
        manager = getattr(self, '_manager', None)
        if manager:
            manager._coerce_datastreams(self.datastreams, datastreams)
        self._data['datastreams'] = datastreams

    def update(self, fields=None):
        """Updates feed and datastreams via the API.

        If successful, the current datastream values are stored and any changes
        in feed metadata overwrite previous values. Cosm stores a server-side
        timestamp in the "updated" attribute and sets the feed to "live" if it
        wasn't before.

        :param fields: If given, only update these fields.
        :type fields: list of strings

        """
        url = self.feed
        state = self.__getstate__()
        if fields is not None:
            fields = set(fields)
            state = {k: v for k, v in state.items() if k in fields}
        self._manager.update(url, **state)

    def delete(self):
        """Delete this feed via the API.

        .. warning:: This is final and cannot be undone.

        """
        url = self.feed
        self._manager.delete(url)


class Datastream(Base):
    """Cosm Datastream containing current and historical values."""

    _datapoints = None

    def __init__(self, id, **kwargs):
        """Create a new datastream object locally."""
        self._data = {'id': id}
        self.datapoints = kwargs.pop('datapoints', [])
        self._data.update(**kwargs)

    def __getstate__(self):
        state = super(Datastream, self).__getstate__()
        if not state['datapoints']:
            state.pop('datapoints')
        return state

    def __repr__(self):
        return "<{}.{}({id!r})>".format(
            __package__, self.__class__.__name__, id=self._data.get('id'))

    @property
    def datapoints(self):
        """Manager for datapoints of this datastream."""
        if self._datapoints is None:
            import cosm.api
            self._datapoints = cosm.api.DatapointsManager(self)
        return self._datapoints

    @datapoints.setter  # NOQA
    def datapoints(self, datapoints):
        self._data['datapoints'] = datapoints

    def update(self, fields=None):
        """Send the current state of this datastream to Cosm."""
        state = self.__getstate__()
        if fields is not None:
            fields = set(fields)
            state = {k: v for k, v in state.items() if k in fields}
        self._manager.update(self.id, **state)

    def delete(self):
        """Delete this datastream from Cosm."""
        self._manager.delete(self.id)


class Datapoint(Base):
    """A Datapoint represents a value at a certain point in time."""

    def __init__(self, at, value):
        """Create a new datapoint locally."""
        super(Datapoint, self).__init__()
        self._data['at'] = at
        self._data['value'] = value

    def __repr__(self):
        classname = 'cosm.' + self.__class__.__name__
        return "{}({!r}, {!r})".format(classname, self.at, self.value)

    def update(self):
        """Update this datapoint's value."""
        state = self.__getstate__()
        self._manager.update(state.pop('at'), **state)

    def delete(self):
        """Delete this datapoint."""
        self._manager.delete(self.at)


class Location(Base):
    """The location and location type of a feed."""

    def __init__(self, name=None, domain=None, exposure=None, disposition=None,
                 lat=None, lon=None, ele=None, waypoints=None):
        """Create a local location instance."""
        self._data = {
            'name': name,
            'domain': domain,
            'exposure': exposure,
            'disposition': disposition,
            'lat': lat,
            'lon': lon,
            'ele': ele,
        }
        if waypoints is not None:
            self._data['waypoints'] = waypoints


class Waypoint(Base):
    """A waypoint represents where a mobile feed was at a particular time."""

    def __init__(self, at, lat, lon):
        """Create a location waypoint, a timestamped cordinate pair."""
        self._data = {
            'at': at,
            'lat': lat,
            'lon': lon,
        }


class Trigger(Base):
    """Triggers provide 'push' capabilities (aka notifications).

    To create a new trigger, use the :class:`~cosm.api.TriggersManager` on a
    :class:`~cosm.api.CosmAPIClient` instance.

    >>> from cosm import CosmAPIClient
    >>> api = CosmAPIClient("API_KEY")
    >>> api.triggers.create(123, "temperature", "http://example.com", "frozen")
    <Trigger(123, 'temperature', 'http://example.com', 'frozen')>

    """

    def __init__(self, environment_id, stream_id, url, trigger_type,
                 threshold_value=None, **kwargs):
        self._data = {
            'environment_id': environment_id,
            'stream_id': stream_id,
            'url': url,
            'trigger_type': trigger_type,
        }
        if threshold_value is not None:
            self._data['threshold_value'] = threshold_value
        self._data.update(kwargs)

    def __repr__(self):
        r = "<{}({environment_id!r}, {stream_id!r}, {url!r}, {trigger_type!r})>"
        return r.format(self.__class__.__name__, **self._data)

    def update(self, fields=None):
        """Update an existing trigger."""
        state = self.__getstate__()
        state.pop('id', None)
        if fields is not None:
            fields = set(fields)
            state = {k: v for k, v in state.items() if k in fields}
        self._manager.update(self.id, **state)

    def delete(self):
        """Delete a trigger."""
        self._manager.delete(self.id)


class Key(Base):
    """Keys set which permissions are granted for certain resources."""

    def __init__(self, label, permissions, expires_at=None,
                 private_access=False):
        self._data = {
            'label': label,
            'permissions': permissions,
            'private_access': private_access,
        }
        if expires_at:
            self._data['expires_at'] = expires_at

    def delete(self):
        """Delete this key."""
        self._manager.delete(self.api_key)


class Permission(Base):
    """Permissions restrict what can be done by a key."""

    def __init__(self, access_methods, source_ip=None, referer=None,
                 minimum_interval=None, label=None, resources=None):
        self._data = {
            'access_methods': access_methods,
        }
        self._data.update((name, value) for (name, value) in (
            ('source_ip', source_ip),
            ('referer', referer),
            ('minimum_interval', minimum_interval),
            ('label', label),
            ('resources', resources),
        ) if value is not None)


class Resource(Base):
    """A Resource defines what an API key has access to."""

    def __init__(self, feed_id, datastream_id=None):
        self._data = {
            'feed_id': feed_id,
        }
        if datastream_id:
            self._data['datastream_id'] = datastream_id

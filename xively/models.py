# -*- coding: utf-8 -*-

__title__ = 'xively-python'
__version__ = '0.1.0-rc2'


__all__ = ['Feed', 'Datastream', 'Datapoint', 'Location', 'Waypoint',
           'Trigger', 'Key', 'Permission', 'Resource']


class Base(object):
    """Abstract base class to store API data and allow (de)serialisation."""

    def __init__(self):
        self._data = {}

    def __getstate__(self):
        """Returns the current state of the object.

        This is the data that should be sent to the Xively API.
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
    """Xively Feed, which can contain a number of Datastreams.

    :param title: A descriptive name for the feed
    :param description: A longer text description of the feed
    :param website: The URL of a website which is relevant to this feed e.g.
        home page
    :param email: A public contact email address for the provider of this feed
    :param tags: Tagged metadata about the environment (characters ' " and
        commas will be stripped out)
    :param location: :class:`.Location` object for this feed
    :param private: Whether the environment is private or not.
    :type private: bool

    Usage::

        >>> import xively
        >>> xively.Feed(title="Xively Office environment")
        <xively.Feed(None)>

    """

    VERSION = "1.0.0"

    # Set id and feed directly as they aren't part of state. By setting them on
    # the class they won't get entered into _data and will be set on the
    # instance itself.
    id = None
    feed = None

    _datastreams_manager = None

    def __init__(self, title, description=None, website=None, email=None,
                 tags=None, location=None, private=None, datastreams=None):
        """Creates a new Feed."""
        self._data = {
            'version': self.VERSION,
            'title': title,
            'description': description,
            'website': website,
            'email': email,
            'tags': tags,
            'location': location,
            'private': private,
        }
        if datastreams is not None:
            self.datastreams = datastreams

    def __repr__(self):
        return "<{}.{}({id})>".format(
            __package__, self.__class__.__name__, id=self.id)

    @property
    def datastreams(self):
        """Manager for datastreams of this feed.

        When fetched from the API, datastreams behaves like a cache, populated
        with the most recently updated datastreams for this feed. The manager
        can also be used to create, update and delete datastreams for this
        feed.

        Usage::

            >>> import xively
            >>> api = xively.XivelyAPIClient("API_KEY")
            >>> feed = api.feeds.get(7021)
            >>> feed.datastreams[0]  # doctest: +IGNORE_UNICODE
            <xively.Datastream('3')>

        """
        if self._datastreams_manager is None:
            import xively.managers
            self._datastreams_manager = xively.managers.DatastreamsManager(self)
        return self._datastreams_manager

    @datastreams.setter  # NOQA
    def datastreams(self, datastreams):
        manager = getattr(self, '_manager', None)
        if manager:
            # Accessing self.datastreams will create a DatastreamsManager if
            # one didn't already exist.
            manager._coerce_datastreams(datastreams, self.datastreams)
        self._data['datastreams'] = datastreams

    def update(self, fields=None):
        """Updates feed and datastreams via the API.

        If successful, the current datastream values are stored and any changes
        in feed metadata overwrite previous values. Xively stores a server-side
        timestamp in the "updated" attribute and sets the feed to "live" if it
        wasn't before.

        :param fields: If given, only update these fields.
        :type fields: list of strings

        """
        url = self.id
        state = self.__getstate__()
        if fields is not None:
            fields = set(fields)
            state = {k: v for k, v in state.items() if k in fields}
        self._manager.update(url, **state)

    def delete(self):
        """Delete this feed via the API.

        .. warning:: This is final and cannot be undone.

        """
        url = self.id
        self._manager.delete(url)


class Datastream(Base):
    """Xively Datastream containing current and historical values.

    :param id: The ID of the datastream
    :param tags: Tagged metadata about the datastream
    :param unit: The :class:`.Unit` of the datastream
    :param min_value: The minimum value since the last reset
    :param max_value: The maximum value since the last reset
    :param current_value: The current value of the datastream
    :param at: The timestamp of the current value
    :param datapoints: A collection of timestamped values

    """

    _datapoints_manager = None

    def __init__(self, id, tags=None, unit=None, min_value=None,
                 max_value=None, current_value=None, datapoints=None, at=None):
        """Creates a new datastream object locally."""
        self._data = {
            'id': id,
            'tags': tags,
            'unit': unit,
            'min_value': min_value,
            'max_value': max_value,
            'current_value': current_value,
            'at': at,
        }
        self.datapoints = datapoints or []

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
        """Manager for datapoints of this datastream.

        When a datastream is fetched with history from the API, datapoints is
        a sequence of timestamped values for the period requested. The manger
        can also be used tocreate, update and delte datapoints for this
        datastream.

        Usage::

            >>> import xively
            >>> import datetime
            >>> api = xively.XivelyAPIClient("API_KEY")
            >>> feed = api.feeds.get(7021)
            >>> datastream = feed.datastreams.get("random5",
            ...     start=datetime.datetime(2013, 1, 1, 14, 0, 0),
            ...     end=datetime.datetime(2013, 1, 1, 16, 0, 0))
            >>> datastream.datapoints[:2]
            ... # doctest: +IGNORE_UNICODE +NORMALIZE_WHITESPACE +ELLIPSIS
            [xively.Datapoint(datetime.datetime(...), '0.25741970'),
             xively.Datapoint(datetime.datetime(...), '0.86826886')]

        """
        if self._datapoints_manager is None:
            import xively.managers
            self._datapoints_manager = xively.managers.DatapointsManager(self)
        return self._datapoints_manager

    @datapoints.setter  # NOQA
    def datapoints(self, datapoints):
        self._data['datapoints'] = datapoints

    def update(self, fields=None):
        """Sends the current state of this datastream to Xively.

        This method updates just the single datastream.

        :param fields: If given, only update these fields.
        :type fields: list of strings

        """
        state = self.__getstate__()
        if fields is not None:
            fields = set(fields)
            state = {k: v for k, v in state.items() if k in fields}
        self._manager.update(self.id, **state)

    def delete(self):
        """Delete this datastream from Xively.

        .. warning:: This is final and cannot be undone.

        """
        self._manager.delete(self.id)


class Datapoint(Base):
    """A Datapoint represents a value at a certain point in time.

    :param at: The timestamp of the datapoint
    :param value: The value at this time

    """

    def __init__(self, at, value):
        """Create a new datapoint locally."""
        super(Datapoint, self).__init__()
        self._data['at'] = at
        self._data['value'] = value

    def __repr__(self):
        classname = 'xively.' + self.__class__.__name__
        return "{}({!r}, {!r})".format(classname, self.at, self.value)

    def update(self):
        """Update this datapoint's value."""
        state = self.__getstate__()
        self._manager.update(state.pop('at'), **state)

    def delete(self):
        """Delete this datapoint.

        .. warning:: This is final and cannot be undone.

        """
        self._manager.delete(self.at)


class Location(Base):
    """The location and location type of a feed.

    :param name: The name of the location
    :param domain: The domain of the location, i.e. 'physical' or 'virtual'
    :param exposure: Whether the location is indoors or outdoors
    :param disposition: Whether the location is mobile or static
    :param lat: The latitude of the feed
    :param lon: The longitude of the feed
    :param ele: The elevation of the feed
    :param waypoints: A list of locations for a mobile feed

    """

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
    """A waypoint represents where a mobile feed was at a particular time.

    :param at: The timestamp of the waypoint
    :param lat: The latitude at that time
    :param lon: The longitude at that time

    """

    def __init__(self, at, lat, lon):
        """Create a location waypoint, a timestamped cordinate pair."""
        self._data = {
            'at': at,
            'lat': lat,
            'lon': lon,
        }


class Unit(Base):
    """A type, label and symbol of a values unit."""

    def __init__(self, label=None, type=None, symbol=None):
        self._data = {
            'label': label,
            'type': type,
            'symbol': symbol,
        }


class Trigger(Base):
    """Triggers provide 'push' capabilities (aka notifications).

    To create a new trigger, use the :class:`~xively.api.TriggersManager` on a
    :class:`~xively.api.XivelyAPIClient` instance.

    >>> from xively import XivelyAPIClient
    >>> api = XivelyAPIClient("API_KEY")
    >>> api.triggers.create(123, "temperature", "http://example.com", "frozen")
    <xively.Trigger(3)>

    """

    def __init__(self, environment_id, stream_id, url, trigger_type,
                 threshold_value=None):
        self._data = {
            'environment_id': environment_id,
            'stream_id': stream_id,
            'url': url,
            'trigger_type': trigger_type,
        }
        if threshold_value is not None:
            self._data['threshold_value'] = threshold_value

    def __repr__(self):
        return "<{}.{}({id!r})>".format(
            __package__, self.__class__.__name__, id=self.id)

    def update(self, fields=None):
        """Update an existing trigger.

        :param fields: If given, only update these fields
        :type fields: list of strings

        """
        state = self.__getstate__()
        state.pop('id', None)
        if fields is not None:
            fields = set(fields)
            state = {k: v for k, v in state.items() if k in fields}
        self._manager.update(self.id, **state)

    def delete(self):
        """Delete a trigger.

        .. warning:: This is final and cannot be undone.

        """
        self._manager.delete(self.id)


class Key(Base):
    """Keys set which permissions are granted for certain resources.

    :param label: A label by which the key can be referenced
    :param permissions: Collection of Permission objects controlling the access
                        level
    :param expires_at: Expiry date for the key after which it won't work
    :param private_access: Flag that indicates whether this key can access
                           private resources belonging to the user

    """

    def __init__(self, label, permissions, expires_at=None,
                 private_access=False):
        self._data = {
            'label': label,
            'permissions': permissions,
            'private_access': private_access,
        }
        if expires_at:
            self._data['expires_at'] = expires_at

    def __repr__(self):
        return "<{}.{}({label!r})>".format(
            __package__, self.__class__.__name__, label=self.label)

    def delete(self):
        """Delete this key."""
        self._manager.delete(self.api_key)


class Permission(Base):
    """Permissions restrict what can be done by a key.

    :param access_methods:
        A list containing one or more of [get, put, post, delete] indicating
        what type of access the key has
    :param source_ip:
        An IP address that access should be restricted to, so if specified,
        only requests coming from this IP address will be permitted
    :param referer:
        The referer domain. If present this key will only be able to be
        embedded in a web page with the matching URL.  Subdomains are treated
        as different domains
    :param minimum_interval:
        Can be used to create a key that can only request data with a certain
        resolution, i.e. a key could be created that only displays graphs with
        daily values when embedded in a web page. The same key could not be
        used to access full resolution data
    :param label:
        Optional label for identifying permission set
    :param resources:
        Optional collection of Resource objects restricting access to specific
        feeds or datastreams

    """

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
    """A Resource defines what an API key has access to.

    :param feed_id:
        Reference to a specific feed id
    :param datastream_id:
        Reference to a specific datastream id within a feed. If specified then
        the feed id must also be specified

    """

    def __init__(self, feed_id, datastream_id=None):
        self._data = {
            'feed_id': feed_id,
        }
        if datastream_id:
            self._data['datastream_id'] = datastream_id

# -*- coding: utf-8 -*-

from collections import Sequence
from datetime import datetime

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin  # NOQA

from xively.models import (
    Datapoint,
    Datastream,
    Feed,
    Key,
    Location,
    Permission,
    Resource,
    Trigger,
    Unit,
    Waypoint,
)


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

    def url(self, id_or_url=None):
        """Return a url relative to the base url."""
        url = self.base_url
        if id_or_url:
            url = urljoin(url + '/', str(id_or_url))
        return url

    def _parse_datetime(self, value):
        """Parse and return a datetime string from the Xively API."""
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")

    def _prepare_params(self, params):
        """Prepare parameters to be passed in query strings to the Xively API."""
        params = dict(params)
        for name, value in params.items():
            if isinstance(value, datetime):
                params[name] = value.isoformat() + 'Z'
        return params


class FeedsManager(ManagerBase):
    """Create, update and return Feed objects.

    .. note:: This manager should live on a :class:`.XivelyAPIClient` instance
        and not instantiated directly.

    :param client: Low level :class:`.Client` instance

    Usage::

        >>> import xively
        >>> api = xively.XivelyAPIClient("API_KEY")
        >>> api.feeds.create(title="Xively Office environment")
        <xively.Feed(7021)>
        >>> api.feeds.get(7021)
        <xively.Feed(7021)>
        >>> api.feeds.update(7021, private=True)
        >>> api.feeds.delete(7021)

    """

    resource = 'feeds'

    # List of fields that can be returned from the API but not directly set.
    _readonly_fields = (
        'id',
        'feed',
        'status',
        'creator',
        'created',
        'updated',
        'version',
        'auto_feed_url',
        'product_id',
        'device_serial',
    )

    def __init__(self, client):
        self.client = client
        self.base_url = client.base_url + self.resource

    def create(self, title, description=None, website=None, email=None,
               tags=None, location=None, private=None, datastreams=None):
        """Creates a new Feed.

        :param title: A descriptive name for the feed
        :param description: A longer text description of the feed
        :param website: The URL of a website which is relevant to this feed
            e.g. home page
        :param email: A public contact email address for the creator of this
            feed
        :param tags: Tagged metadata about the environment (characters ' " and
            commas will be stripped out)
        :param location: :class:`.Location` object for this feed
        :param private: Whether the environment is private or not. Can be
            either True or False

        """
        data = {
            'version': Feed.VERSION,
            'title': title,
            'description': description,
            'website': website,
            'email': email,
            'tags': tags,
            'location': location,
            'private': private,
            'datastreams': datastreams,
        }
        feed = self._coerce_feed(data)
        response = self.client.post(self.url(), data=feed)
        response.raise_for_status()
        location = response.headers['location']
        feed.feed = location
        feed.id = _id_from_url(location)
        return feed

    def update(self, id_or_url, **kwargs):
        """Updates an existing feed by its id or url.

        :param id_or_url: The id of a :class:`.Feed` or its URL
        :param kwargs: The fields to be updated

        """
        url = self.url(id_or_url)
        response = self.client.put(url, data=kwargs)
        response.raise_for_status()

    def list(self, page=None, per_page=None, content=None, q=None, tag=None,
             user=None, units=None, status=None, order=None, show_user=None,
             lat=None, lon=None, distance=None, distance_units=None):
        """Returns a paged list of feeds.

        Only feeds that are viewable by the authenticated account will be
        returned. The following parameters can be applied to limit or refine
        the returned feeds:

        :param page: Integer indicating which page of results you are
            requesting. Starts from 1.
        :param per_page: Integer defining how many results to return per page
            (1 to 1000)
        :param content: String parameter ('full' or 'summary') describing
            whether we want full or summary results. Full results means all
            datastream values are returned, summary just returns the
            environment meta data for each feed
        :param q: Full text search parameter. Should return any feeds matching
            this string
        :param tag: Returns feeds containing datastreams tagged with the search
            query
        :param user: Returns feeds created by the user specified
        :param units: Returns feeds containing datastreams with units specified
            by the search query
        :param status: Possible values ('live', 'frozen', or 'all'). Whether to
            search for only live feeds, only frozen feeds, or all feeds.
            Defaults to all
        :param order: Order of returned feeds. Possible values ('created_at',
            'retrieved_at', or 'relevance')
        :param show_user: Include user login and user level for each feed.
            Possible values: true, false (default)

        The following additional parameters are available which allow location
        based searching of feeds:

        :param lat: Used to find feeds located around this latitude
        :param lon: Used to find feeds located around this longitude
        :param distance: search radius
        :param distance_units: miles or kms (default)

        """
        url = self.url()
        params = {k: v for k, v in (
            ('page', page),
            ('per_page', per_page),
            ('content', content),
            ('q', q),
            ('tag', tag),
            ('user', user),
            ('units', units),
            ('status', status),
            ('order', order),
            ('show_user', show_user),
            ('lat', lat),
            ('lon', lon),
            ('distance', distance),
            ('distance_units', distance_units),
        ) if v is not None}
        response = self.client.get(url, params=params)
        response.raise_for_status()
        json = response.json()
        feeds = [self._coerce_feed(feed_data) for feed_data in json['results']]
        return feeds

    def get(self, id_or_url, datastreams=None, show_user=None, start=None,
            end=None, duration=None, find_previous=None, limit=None,
            interval_type=None, interval=None):
        """Fetches and returns a feed by id or url.

        By default the most recent datastreams are returned. It is also
        possible to filter the datastreams returned with the feed by using the
        "datastreams" parameter and a list of datastream IDs.

        :param datastreams: Filter the returned datastreams
        :type datastreams: list of datastream IDs
        :param show_user: Include user login for each feed. (default: False)
        :type show_user: bool

        :param start: Defines the starting point of the query
        :param end: Defines the end point of the data returned
        :param duration: Specifies the duration of the query
        :param find_previous:
            Will also return the previous value to the date range being
            requested.
        :param limit:
            Limits the number of results to the number specified.  Defaults to
            100 and has a maximum of 1000.
        :param interval_type:
            If set to "discrete" the data will be returned in fixed time
            interval format according to the inverval value supplied. If this
            is not set, the raw datapoints will be returned.
        :param interval:
            Determines what interval of data is requested and is defined in
            seconds between the datapoints. If a value is passed in which does
            not match one of these values, it is rounded up to the next value.

        See :meth:`~.DatapointsManager.history` for details.

        """
        url = self.url(id_or_url)
        if isinstance(datastreams, Sequence):
            datastreams = ','.join(datastreams)
        params = {k: v for k, v in (
            ('datastreams', datastreams),
            ('show_user', show_user),
            ('start', start),
            ('end', end),
            ('duration', duration),
            ('find_previous', find_previous),
            ('limit', limit),
            ('interval_type', interval_type),
            ('interval', interval),
        ) if v is not None}
        params = self._prepare_params(params)
        response = self.client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        feed = self._coerce_feed(data)
        return feed

    def delete(self, id_or_url):
        """Delete a feed by id or url.

        .. WARNING:: This is final and cannot be undone.

        :param id_or_url: The feed ID  or its URL

        """
        url = self.url(id_or_url)
        response = self.client.delete(url)
        response.raise_for_status()

    def _coerce_feed(self, feed_data):
        """Returns a Feed object from a mapping object (dict)."""
        datastreams_data = feed_data.pop('datastreams', None)
        location_data = feed_data.pop('location', None)
        # Strip out the readonly fields and manually set later.
        readonly = {f: feed_data.pop(f)
                    for f in self._readonly_fields
                    if f in feed_data}
        feed = Feed(**feed_data)
        feed._manager = self
        feed.id = readonly.pop('id', None)
        feed.feed = readonly.pop('feed', None) or self.url(feed.id)
        # Explicitely set the readonly fields we stripped out earlier.
        for name, value in readonly.items():
            setattr(feed, name, value)
        if datastreams_data:
            feed._datastreams_manager = DatastreamsManager(feed)
            feed.datastreams = self._coerce_datastreams(
                datastreams_data, feed._datastreams_manager)
        if location_data:
            location = self._coerce_location(location_data)
        else:
            location = Location()
        feed._data['location'] = location
        return feed

    def _coerce_datastreams(self, datastreams_data, datastreams_manager):
        """Returns Datastream objects from the data given."""
        datastreams = []
        for data in datastreams_data:
            datastream = datastreams_manager._coerce_datastream(data)
            datastreams.append(datastream)
        return datastreams

    def _coerce_location(self, instance):
        """Returns a Location object, converted from instance if required."""
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
        """Returns a list of Waypoint objects from the given waypoint data."""
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

    :param feed: A :class:`.Feed` instance.

    Usage::

        >>> import xively
        >>> api = xively.XivelyAPIClient("API_KEY")
        >>> feed = api.feeds.get(7021)
        >>> list(feed.datastreams)  # doctest: +IGNORE_UNICODE
        [<xively.Datastream('3')>, <xively.Datastream('4')>]
        >>> feed.datastreams.create("1")
        <xively.Datastream('1')>

    """

    resource = 'datastreams'

    # List of fields that can be returned from the API but not directly set.
    _readonly_fields = (
        'at',
        'current_value',
    )

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

    def create(self, id, current_value=None, tags=None, unit=None,
               min_value=None, max_value=None, at=None):
        """Creates a new datastream on a feed.

        :param id: The ID of the datastream
        :param current_value: The current value of the datastream
        :param tags: Tagged metadata about the datastream
        :param unit: The :class:`.Unit` for this datastream
        :param min_value: The minimum value since the last reset
        :param max_value: The maximum value since the last reset
        :param at: The timestamp of the current value
        :returns: A :class:`.Datastream` object

        """
        datastream_data = dict(
            id=id,
            current_value=current_value,
            tags=tags,
            unit=unit,
            min_value=min_value,
            max_value=max_value,
            at=at)
        datastream = self._coerce_datastream(datastream_data)
        data = {
            'version': self.parent.version,
            'datastreams': [datastream],
        }
        response = self.client.post(self.url(), data=data)
        response.raise_for_status()
        return datastream

    def update(self, datastream_id, **kwargs):
        """Updates a feeds datastream by id.

        :param datastream_id: The ID of the datastream to update
        :param kwargs: The datastream fields to be updated

        """
        url = self.url(datastream_id)
        response = self.client.put(url, data=kwargs)
        response.raise_for_status()

    def list(self, datastreams=None, show_user=None):
        """Returns a list of datastreams for the parent feed object.

        :param datastreams: Filter the returned datastreams
        :type datastreams: list of datastream IDs
        :param show_user: Include user login for each feed (default: False)
        :type show_user: bool

        """
        url = self.url('..')
        params = {k: v for k, v in (
            ('datastreams', datastreams),
            ('show_user', show_user),
        ) if v is not None}
        response = self.client.get(url, params=params)
        response.raise_for_status()
        json = response.json()
        for datastream_data in json.get('datastreams', []):
            datastream = self._coerce_datastream(datastream_data)
            yield datastream

    def get(self, id_or_url, start=None, end=None, duration=None,
            find_previous=None, limit=None, interval_type=None, interval=None):
        """Fetches and returns a feed's datastream by its id.

        If start, end or duration are given, also returns Datapoints for that
        period.

        :param id_or_url: The ID of the datastream to retrieve or its URL
        :param start: Defines the starting point of the query
        :param end: Defines the end point of the data returned
        :param duration: Specifies the duration of the query
        :param find_previous:
            Will also return the previous value to the date range being
            requested.
        :param limit:
            Limits the number of results to the number specified.  Defaults to
            100 and has a maximum of 1000.
        :param interval_type:
            If set to "discrete" the data will be returned in fixed time
            interval format according to the inverval value supplied. If this
            is not set, the raw datapoints will be returned.
        :param interval:
            Determines what interval of data is requested and is defined in
            seconds between the datapoints. If a value is passed in which does
            not match one of these values, it is rounded up to the next value.

        See :meth:`~.DatapointsManager.history` for details.

        """
        url = self.url(id_or_url)
        params = {k: v for k, v in (
            ('start', start),
            ('end', end),
            ('duration', duration),
            ('find_previous', find_previous),
            ('limit', limit),
            ('interval_type', interval_type),
            ('interval', interval),
        ) if v is not None}
        params = self._prepare_params(params)
        response = self.client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        datastream = self._coerce_datastream(data)
        return datastream

    def delete(self, id_or_url):
        """Delete a datastream by id or url.

        .. WARNING:: This is final and cannot be undone.

        :param id_or_url: The datastream ID or its URL

        """
        url = self.url(id_or_url)
        response = self.client.delete(url)
        response.raise_for_status()

    def _coerce_datapoints(self, datapoints_manager, datapoints_data):
        """Returns Datapoints objects from a list of mapping objects (dict)."""
        datapoints = []
        for data in datapoints_data:
            data['at'] = self._parse_datetime(data['at'])
            datapoint = datapoints_manager._coerce_datapoint(data)
            datapoints.append(datapoint)
        return datapoints

    def _coerce_unit(self, instance):
        """Returns a Unit object, converted from instance if required."""
        if isinstance(instance, Unit):
            unit = instance
        else:
            instance_data = dict(**instance)
            unit = Unit(**instance_data)
        return unit

    def _coerce_datastream(self, d):
        """Returns a Datastream object from a mapping object (dict)."""
        if isinstance(d, dict):
            datapoints_data = d.pop('datapoints', None)
            unit_data = d.pop('unit', None)
            # Remove version, part of Feed not Datastream
            d.pop('version', None)
            # Strip out the readonly fields and manually set later.
            readonly = {f: d.pop(f) for f in self._readonly_fields if f in d}
            datastream = Datastream(**d)
            # Explicitely set the readonly fields we stripped out earlier.
            for name, value in readonly.items():
                setattr(datastream, name, value)
            if datapoints_data:
                datapoints = self._coerce_datapoints(
                    datastream.datapoints, datapoints_data)
                datastream.datapoints = datapoints
            if unit_data:
                unit = self._coerce_unit(unit_data)
                datastream.unit = unit
        elif isinstance(d, Datastream):
            datastream = d
        datastream._manager = self
        return datastream


class DatapointsManager(Sequence, ManagerBase):
    """Manage datapoints of a datastream.

    A list of :class:`.Datapoint` objects can be retrieved along with the
    :class:`.Datastream` (or :class:`.Feed`) which can be accessed via this
    instance as a sequence.

    :param datastream: A :class:`.Datastream` instance.

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

    def create(self, value, at=None):
        """Create a single new datapoint for this datastream.

        :param at: The timestamp of the datapoint (default: datetime.now())
        :param value: The value at this time

        To create multiple datapoints at the same time do the following
        instead:

        .. note:: You can use ISO8601 formatted strings instead of datetime
                  objects when dealing with the API.

        >>> import xively
        >>> api = xively.XivelyAPIClient("API_KEY")
        >>> feed = api.feeds.get(7021)
        >>> datastream = feed.datastreams[0]
        >>> # First create the datapoints.
        >>> datastream.datapoints = [
        ...     xively.Datapoint(at="2010-05-20T11:01:43Z", value=294),
        ...     xively.Datapoint(at="2010-05-20T11:01:44Z", value=295),
        ...     xively.Datapoint(at="2010-05-20T11:01:45Z", value=296),
        ...     xively.Datapoint(at="2010-05-20T11:01:46Z", value=297),
        ... ]
        >>> # Then send them to the server.
        >>> datastream.update(fields='datapoints')

        """
        at = at or datetime.now()
        datapoint = Datapoint(at, value)
        payload = {'datapoints': [datapoint]}
        response = self.client.post(self.url(), data=payload)
        response.raise_for_status()
        return datapoint

    def update(self, at, value):
        """Update the value of a datapiont at a given timestamp.

        :param at: The timestamp of a value to change
        :param value: The value to change

        .. note:: A datapoint at the given time must already exist.

        """
        url = "{}/{}Z".format(self.url(), at.isoformat())
        payload = {'value': value}
        response = self.client.put(url, data=payload)
        response.raise_for_status()

    def get(self, at):
        """Fetch and return a :class:`.Datapoint` at the given timestamp.

        :param at: The timestamp to return a datapoint for

        """
        url = "{}/{}Z".format(self.url(), at.isoformat())
        response = self.client.get(url)
        response.raise_for_status()
        data = response.json()
        data['at'] = self._parse_datetime(data['at'])
        return self._coerce_datapoint(data)

    def history(self, start=None, end=None, duration=None, find_previous=None,
                limit=None, interval_type=None, interval=None):
        """Fetch and return a list of datapoints in a given timerange.

        :param start: Defines the starting point of the query
        :param end: Defines the end point of the data returned
        :param duration: Specifies the duration of the query
        :param find_previous:
            Will also return the previous value to the date range being
            requested.
        :param limit:
            Limits the number of results to the number specified.  Defaults to
            100 and has a maximum of 1000.
        :param interval_type:
            If set to "discrete" the data will be returned in fixed time
            interval format according to the inverval value supplied. If this
            is not set, the raw datapoints will be returned.
        :param interval:
            Determines what interval of data is requested and is defined in
            seconds between the datapoints. If a value is passed in which does
            not match one of these values, it is rounded up to the next value.

        .. note::

            ``find_previous`` is useful for any graphing because if you
            want to draw a graph of the date range you specified you would end
            up with a small gap until the first value.

        .. note::

            In order to paginate through the data use the last timestamp
            returned as the start of the next query.

        .. note::

            The maximum number of datapoints able to be returned from the API
            in one query is 1000. If you need more than 1000 datapoints for
            a specific period you should use the start and end times to split
            them up into smaller chunks.

        The valid time units are::

        * seconds
        * minute(s)
        * hour(s)
        * day(s)
        * week(s)
        * month(s)
        * year(s)

        The acceptable intervals are currently:

        ===== ============================== ==========================
        Value Description                    Maximum range in one query
        ===== ============================== ==========================
        0     Every datapoint stored         6 hours
        30    One datapoint every 30 seconds 12 hours
        60    One datapoint every minute     24 hours
        300   One datapoint every 5 minutes  5 days
        900   One datapoint every 15 minutes 14 days
        1800  One datapoint per 30 minutes   31 days
        3600  One datapoint per hour         31 days
        10800 One datapoint per three hours  90 days
        21600 One datapoint per six hours    180 days
        43200 One datapoint per twelve hours 1 year
        86400 One datapoint per day          1 year
        ===== ============================== ==========================

        """
        url = self.url('..').rstrip('/')
        params = {k: v for k, v in (
            ('start', start),
            ('end', end),
            ('duration', duration),
            ('find_previous', find_previous),
            ('limit', limit),
            ('interval_type', interval_type),
            ('interval', interval),
        ) if v is not None}
        params = self._prepare_params(params)
        response = self.client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        for datapoint_data in data.get('datapoints', []):
            datapoint_data['at'] = self._parse_datetime(datapoint_data['at'])
            yield self._coerce_datapoint(datapoint_data)

    def delete(self, at=None, start=None, end=None, duration=None):
        """Delete a datapoint or a range of datapoints.

        :param at: A timestamp of a single datapoint to delete
        :param start: Defines the starting point of the query
        :param end: Defines the end point of the datapoints deleted
        :param duration: Specifies the duration of the query

        By providing a start and end timestamp as query parameters, you may
        remove all datapoints that lie between those dates. If you send your
        request with only a start timestamp, all datapoints after the value
        will be removed. Providing an end timestamp will remove all datapoints
        prior to the supplied value.

        Additionally, this method supports a duration parameter (e.g.
        ``duration="3hours"``). Providing a `start` and a `duration` will
        delete all datapoints between the `start` and (`start` + `duration`).
        Providing `end` will delete all datapoints between (`end` - `duration`)
        and `end`. The formatting of the `duration` parameter is the same as is
        used in the :meth:`.history` method.

        .. warning: This is final and cannot be undone.

        """
        url = self.url()
        params = {k: v for k, v in (
            ('start', start),
            ('end', end),
            ('duration', duration),
        ) if v is not None}
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

    This manager should live on a :class:`.XivelyAPIClient` instance and not
    instantiated directly.

    :param client: Low level :class:`.Client` instance

    Usage::

        >>> import xively
        >>> api = xively.XivelyAPIClient("API_KEY")
        >>> api.triggers.create(
        ...     environment_id=8470, stream_id="0",
        ...     url="http://www.postbin.org/1ijyltn",
        ...     trigger_type='lt', threshold_value="15.0")
        <xively.Trigger(3)>

    """

    resource = 'triggers'

    _readonly_fields = (
        'id',
        'notified_at',
        'user',
    )

    def __init__(self, client):
        self.client = client
        self.base_url = client.base_url + self.resource

    def create(self, environment_id, stream_id, url, trigger_type,
               threshold_value=None):
        """Create a new :class:`.Trigger`.

        :param environment_id: An ID of a :class:`.Feed`
        :param stream_id: An ID of a :class:`.Datastream`
        :param url: The URL to POST events to
        :param trigger_type: The type of trigger (from below)
        :param threshold_value: The threshold at which the trigger fires

        :returns: A new :class:`.Trigger` object.

        Possible values for ``trigger_type`` are:

        ======= ================================
        gt      greater than
        gte     greater than or equal to
        lt      less than
        lte     less than or equal to
        eq      equal to
        change  any change
        frozen  no updates for 15 minutes
        live    updated again after being frozen
        ======= ================================

        """
        data = {
            'environment_id': environment_id,
            'stream_id': stream_id,
            'url': url,
            'trigger_type': trigger_type,
            'threshold_value': threshold_value,
        }
        trigger = self._coerce_trigger(data)
        response = self.client.post(self.url(), data=trigger)
        response.raise_for_status()
        trigger._manager = self
        location = response.headers['location']
        trigger._data['id'] = int(location.rsplit('/', 1)[1])
        return trigger

    def get(self, id_or_url):
        """Fetch and return an existing trigger.

        :param id_or_url: The ID of the trigger or its URL

        """
        url = self.url(id_or_url)
        response = self.client.get(url)
        response.raise_for_status()
        data = response.json()
        data.pop('id')
        notified_at = data.pop('notified_at', None)
        user = data.pop('user', None)
        trigger = self._coerce_trigger(data)
        trigger._data['id'] = id_or_url
        if notified_at:
            trigger._data['notified_at'] = self._parse_datetime(notified_at)
        if user:
            trigger._data['user'] = user
        trigger._manager = self
        return trigger

    def update(self, id_or_url, **kwargs):
        """Update an existing trigger.

        :param id_or_url: The ID of the :class:`.Trigger` to update or its URL
        :param kwargs: The fields to be updated

        """
        url = self.url(id_or_url)
        response = self.client.put(url, data=kwargs)
        response.raise_for_status()

    def list(self, feed_id=None):
        """Return a list of triggers.

        :param feed_id: Filter the returned triggers to only include those on
                        datastreams of the specified feed.

        """
        url = self.url()
        params = {k: v for k, v in (
            ('feed_id', feed_id),
        ) if v is not None}
        response = self.client.get(url, params=params)
        response.raise_for_status()
        json = response.json()
        for data in json:
            trigger = self._coerce_trigger(data)
            trigger._manager = self
            yield trigger

    def delete(self, id_or_url):
        """Delete a trigger by id or url.

        .. WARNING:: This is final and cannot be undone.

        :param id_or_url: The datastream ID or its URL

        """
        url = self.url(id_or_url)
        response = self.client.delete(url)
        response.raise_for_status()

    def _coerce_trigger(self, d):
        # Strip out the readonly fields and manually set later.
        readonly = {f: d.pop(f) for f in self._readonly_fields if f in d}
        trigger = Trigger(**d)
        # Explicitely set the readonly fields we stripped out earlier.
        for name, value in readonly.items():
            setattr(trigger, name, value)
        return trigger


class KeysManager(ManagerBase):
    """Manage keys their permissions and restrict by resource.

    This manager should live on a :class:`.XivelyAPIClient` instance and not
    instantiated directly.

    :param client: Low level :class:`.Client` instance

    Usage::

        >>> import xively
        >>> api = xively.XivelyAPIClient("API_KEY")
        >>> api.keys.create(
        ...     label="sharing key",
        ...     private_access=True,
        ...     permissions=[
        ...         xively.Permission(
        ...             access_methods=["put"],
        ...             source_ip="128.44.98.129",
        ...             resources=[
        ...                 xively.Resource(feed_id=504),
        ...             ]),
        ...         xively.Permission(access_methods=["get"])
        ...     ])
        <xively.Key('sharing key')>

    """

    resource = 'keys'

    def __init__(self, client):
        self.client = client
        self.base_url = client.base_url + self.resource

    def create(self, label, permissions, expires_at=None, private_access=None):
        """Create a new API key.

        :param label: A label by which the key can be referenced
        :param permissions: Collection of Permission objects controlling the
                            access level
        :param expires_at: Expiry date for the key after which it won't work
        :param private_access: Flag that indicates whether this key can access
                               private resources belonging to the user

        """
        data = dict(label=label, permissions=permissions,
                    expires_at=expires_at, private_access=private_access)
        key = self._coerce_key(data)
        response = self.client.post(self.url(), data={'key': key})
        response.raise_for_status()
        location = response.headers['Location']
        key.api_key = _id_from_url(location)
        return key

    def list(self, feed_id=None):
        """List all API keys for this account or for the given feed.

        :param feed_id: Returns api keys limited to that feed and its
                        datastreams.

        """
        url = self.url()
        params = {}
        if feed_id is not None:
            params['feed_id'] = feed_id
        response = self.client.get(url, params=params)
        response.raise_for_status()
        json = response.json()
        for data in json['keys']:
            key = self._coerce_key(data)
            yield key

    def get(self, key_id):
        """Fetch and return an API key by its id.

        :param key_id: The ID of the key to get.

        .. note: Unless a master API key is used, the only key that can be read
                 is this key. A master key is a non-resource restricted,
                 private key, which has permissions to perform all HTTP
                 methods.

        """
        url = self.url(key_id)
        response = self.client.get(url)
        response.raise_for_status()
        data = response.json()
        key = self._coerce_key(data['key'])
        return key

    def delete(self, key_id):
        """Delete the specified key.

        :param key_id: The key ID

        .. note: You must use a master key to delete an API Key. A master key
                 is a non-resource restricted, private key, which has
                 permissions to perform all HTTP methods.

        """
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

    >>> _id_from_url('http://api.xively.com/v2/feeds/1234')
    '1234'

    """
    id = url.rsplit('/', 1)[1]
    return id


REST API Example
================

    >>> client = xively.api.Client(API_KEY)

Feeds
-----

    >>> feed = client.feeds.create(title="Area 51")
    >>> feed = client.feeds.get(feed.id)
    >>> feed = client.feeds.get(feed.feed)
    >>> feed.private = True
    >>> feed.update()
    >>> feed.delete()
    >>> feed.datastreams[0].datapoints.create(...)

Datastreams
-----------

We only create one datastream at a time.

    >>> datastream = feed.datastreams.create("energy", current_value=42)
    >>> datastream = feed.datastreams.get("energy")
    >>> datastream.current_value = 123
    >>> datastream.update()
    >>> datastream.delete()

Datapoints
----------

    >>> now = datetime.utcnow()
    >>> datapoints = datastream.datapoints.create([
    ...     {'at': now - timedelta(seconds=1), 'value': 42},
    ...     {'at': now, 'value': 43},
    ... ])
    >>> datapoint = datastream.datapoints.get(now)
    >>> datapoint.value = 44
    >>> datapoint.update()
    >>> datapoint.delete()

Historical Queries
------------------

Fetching history of a datastream:

    >>> datapoints = datastream.datapoints.history(end=datetime.utcnow(), duration=1800)

Retrieving a datastream with historical datapoints:

    >>> datastream = feed.datastreams.get("energy", end=datetime.utcnow(), duration="30minutes")
    >>> datapoints = list(datastream.datapoints)

Retrieving a feed and its datastreams with historical datapoints:

    >>> feed = client.feeds.get(feed.id, end=datetime.utcnow(), duration=3600, datastreams=[...])
    >>> print list(feed.datastreams[0].datapoints)
    [Datapoint(...), Datapoint(...), ...]

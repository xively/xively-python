xively-python
=============

.. image:: https://travis-ci.org/xively/xively-python.png?branch=master
    :target: https://travis-ci.org/xively/xively-python
    :alt: Build Status

This is the official pythonic wrapper library for the Xively V2 API.


Create a Feed
-------------

    >>> import xively
    >>> # Connect to the API using your API key.
    >>> api = xively.XivelyAPIClient("API_KEY")
    >>> # Create a new Feed object.
    >>> feed = api.feeds.create(title="My Xively Feed")
    >>> # Let's give it one datastream with id 'temperature'
    >>> datastream = feed.datastreams.create(id='temperature')


Create a Datapoint
------------------

The datapoint creation endpoint takes an array of datapoints

    >>> datastream.datapoints.create(value=42)  # doctest: +ELLIPSIS
    xively.Datapoint(datetime.datetime(...), 42)

Alternatively you can update the datastream's current value and a new datapoint
will be created.

    >>> datastream.current_value = 42
    >>> # We only want to change current_value.
    >>> datastream.update(fields=['current_value'])

Without specifying the fields to update, all fields would be sent to the Xively
API which would include the updated_at field with the time that the old value
was updated. This is probably not what you want but is the intended behaviour
of the API.

Retrieve Feed History
---------------------

This example shows how to fetch the history of all datastreams in a feed.
A simple thing one may wish to do is store those datapoints in a dict of lists.
Let's first import the library, connect to Xively API and fetch test feed:

    >>> import xively
    >>> api = xively.XivelyAPIClient("API_KEY")
    >>> feed = api.feeds.get(61916)

Now we can obtain the history for each of the datastreams and store it as desired:

    >>> history = {}
    >>> for ds in feed.datastreams.list():
    ...   # Retrieve datapoints for the last minute and convert the sequence to a list.
    ...   datapoints = list(ds.datapoints.history(duration='1minute', interval=0))
    ...   # Use datastream ID as the key to store the list of datapoints.
    ...   history[str(ds.id)] = datapoints
    ...

Now we can view the 1 minute history of any given datastream, e.g. 'random5':

    >>> for dp in history['random5']: (str(dp.at), float(dp.value))
    ...
    ('2013-06-21 12:52:40.131143', 0.59272145)
    ('2013-06-21 12:52:45.131372', 0.56624704)
    ('2013-06-21 12:52:50.116811', 0.44327459)
    ('2013-06-21 12:52:55.268417', 0.19339284)
    ('2013-06-21 12:53:00.127861', 0.07447929)
    ('2013-06-21 12:53:05.157432', 0.2296788)
    ('2013-06-21 12:53:10.118524', 0.25192645)
    ('2013-06-21 12:53:15.118767', 0.14700542)
    ('2013-06-21 12:53:20.111343', 0.36844434)
    ('2013-06-21 12:53:25.132045', 0.33328756)
    ('2013-06-21 12:53:30.142814', 0.12248417)
    ('2013-06-21 12:53:35.116271', 0.58426795)
    >>>

.. image :: https://cruel-carlota.pagodabox.com/90b5c954d357acd2dc137d56f8354dd3
    :alt: githalytics.com
    :target: http://githalytics.com/xively/xively-python

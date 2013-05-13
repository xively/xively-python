xively-python
===========

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

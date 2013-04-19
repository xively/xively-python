cosm-python
===========

This is the official pythonic wrapper library for the Cosm V2 API.


Create a Feed
-------------

    >>> import cosm
    >>> # Connect to the API using your API key.
    >>> api = cosm.CosmAPIClient("API_KEY")
    >>> # Create a new Feed object.
    >>> feed = api.feeds.create(title="My Cosm Feed")
    >>> # Let's give it one datastream with id 'temperature'
    >>> datastream = feed.datastreams.create(id='temperature')


Create a Datapoint
------------------

The datapoint creation endpoint takes an array of datapoints

    >>> from datetime import datetime
    >>> datapoint = cosm.Datapoint(at=datetime.now(), value=25)
    >>> datastream.datapoints.create([datapoint])  # doctest: +ELLIPSIS
    [cosm.Datapoint(datetime.datetime(...), 25)]

Alternatively you can update the datastream's current value and a new datapoint
will be created.

    >>> datastream.current_value = 26
    >>> # We only want to change current_value.
    >>> datastream.update(fields=['current_value'])

Without specifying the fields to update, all fields would be sent to the Cosm
API which would include the updated_at field with the time that the old value
was updated. This is probably not what you want but is the intended behaviour
of the API.

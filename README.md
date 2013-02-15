cosm-python
===========

This is the official pythonic wrapper library for the Cosm V2 API.


Create a Feed
-------------

The cosm-python library makes it easy to convert Python objects into Cosm ones.

    >>> import cosm
    >>> # Initialize a new Feed object.
    >>> feed = cosm.Feed(title="My Cosm Feed")
    >>> # Let's give it one datastream with id 'temperature'
    >>> feed.datastreams = [cosm.Datastream(id='temperature')]

Let's create the feed on Cosm

    >>> client = cosm.Client("YOUR_API_KEY")
    >>> response = client.post('/v2/feeds.json', data=feed)
    >>> # Will give us the location of the Cosm feed including the ID.
    >>> print response.headers['Location']
    http://api.cosm.com/v2/feeds/504


Create a Datapoint
------------------

The datapoint creation endpoint takes an array of datapoints

    >>> from datetime import datetime
    >>> datapoint = cosm.Datapoint(at=datetime.now(), value=25)
    >>> client.post('/v2/feeds/504/datastreams/temperature/datapoints',
    ...             data={'datapoints': [datapoint]})
    <Response [200]>

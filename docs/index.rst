.. Xively Python documentation master file, created by
   sphinx-quickstart on Wed Mar 13 18:09:08 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Xively Python's documentation
========================================

xively-python is a wrapper around Xively's REST API to make working with the
connected object cloud easy and pythonic.

The library has been published to PyPI, so installing it should be as simple as
running ``pip install xively-python`` from your command prompt.

Example:

    >>> import xively
    >>> api = xively.XivelyAPIClient("YOUR_API_KEY")
    >>> feed = api.feeds.get(7021)

    >>> # Viewing datapoints
    >>> import datetime
    >>> start = datetime.datetime(2013, 1, 1, 14, 14, 55)
    >>> stream = feed.datastreams[0]
    >>> points = stream.datapoints.history(start=start, duration='1second')
    >>> list(points)  # doctest: +ELLIPSIS +IGNORE_UNICODE
    [xively.Datapoint(datetime.datetime(2013, 1, 1, 14, 14, 55, 118845), '0.25741970'), ...]

    >>> # Updating a feed
    >>> import datetime
    >>> now = datetime.datetime.utcnow()
    >>> feed.datastreams = [
    ...     xively.Datastream(id='sensor1', current_value=37.2, at=now),
    ...     xively.Datastream(id='sensor2', current_value='normal', at=now),
    ...     xively.Datastream(id='sensor3', current_value=19, at=now),
    ... ]
    >>> feed.update()

    >>> # Uploading new points
    >>> import random
    >>> randompoints = [
    ...     xively.Datapoint(datetime.datetime.utcnow(), random.random()),
    ...     xively.Datapoint(datetime.datetime.utcnow(), random.random()),
    ...     xively.Datapoint(datetime.datetime.utcnow(), random.random()),
    ... ]
    >>> stream.datapoints = randompoints
    >>> stream.update(fields='datapoints')


Contents:

.. toctree::
    :maxdepth: 3

    reference.rst
    examples.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


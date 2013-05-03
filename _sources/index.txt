.. Cosm Python documentation master file, created by
   sphinx-quickstart on Wed Mar 13 18:09:08 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Cosm Python's documentation
======================================

cosm-python is a wrapper around Cosm's REST API to make working with the
connected object cloud easy and pythonic.

Example:

    >>> import cosm
    >>> api = cosm.CosmAPIClient("YOUR_API_KEY")
    >>> feed = api.feeds.get(7021)

    >>> # Viewing datapoints
    >>> import datetime
    >>> start = datetime.datetime(2013, 1, 1, 14, 14, 55)
    >>> stream = feed.datastreams[0]
    >>> points = stream.datapoints.history(start=start, duration='1second')
    >>> list(points)  # doctest: +ELLIPSIS +IGNORE_UNICODE
    [cosm.Datapoint(datetime.datetime(2013, 1, 1, 14, 14, 55, 118845), '0.25741970'), ...]

    >>> # Uploading new points
    >>> import random
    >>> randompoints = [
    ...     cosm.Datapoint(datetime.datetime.now(), random.random()),
    ...     cosm.Datapoint(datetime.datetime.now(), random.random()),
    ...     cosm.Datapoint(datetime.datetime.now(), random.random()),
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


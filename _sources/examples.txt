Examples
========

CurrentCost
-----------

This example reads data from a CurrentCost connected via USB. ElementTree is
used to find the temperature, watts and time of day. The script assumes a feed
and two datastreams labelled 'tmpr' and 'watts' have already been created,
a key generated with permissions to upload values for these datastreams.

.. literalinclude:: ../examples/currentcost2xively.py
    :language: python

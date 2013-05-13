=============
API Reference
=============

.. module:: xively

The xively-python library consists of two layers. The top layer uses the
:class:`XivelyAPIClient` and object wrappers.  The lower layer via
:class:`Client` gives access directly to sending native python types and
accessing the response.

API Client
==========

.. autoclass:: xively.XivelyAPIClient
    :members:
    :undoc-members:

Feeds, Datastreams and Datapoints
---------------------------------

.. autoclass:: xively.managers.FeedsManager
    :members:
    :undoc-members:
    :exclude-members: resource

.. autoclass:: xively.Feed
    :members:
    :undoc-members:
    :exclude-members: id, feed

.. autoclass:: xively.managers.DatastreamsManager
    :members:
    :undoc-members:
    :exclude-members: resource

.. autoclass:: xively.Datastream
    :members:
    :undoc-members:

.. autoclass:: xively.managers.DatapointsManager
    :members:
    :undoc-members:
    :exclude-members: resource

.. autoclass:: xively.Datapoint
    :members:
    :undoc-members:

Location and Waypoints
----------------------

.. autoclass:: xively.Location
    :members:
    :undoc-members:

.. autoclass:: xively.Waypoint
    :members:
    :undoc-members:

API Keys
--------

.. autoclass:: xively.managers.KeysManager
    :members:
    :undoc-members:

.. autoclass:: xively.Key
    :members:
    :undoc-members:

.. autoclass:: xively.Permission
    :members:
    :undoc-members:

.. autoclass:: xively.Resource
    :members:
    :undoc-members:

Triggers
--------

.. autoclass:: xively.managers.TriggersManager
    :members:
    :undoc-members:
    :exclude-members: resource

.. autoclass:: xively.Trigger
    :members:
    :undoc-members:

Low Level Client
================

.. autoclass:: xively.Client
    :members:
    :undoc-members:
    :show-inheritance:
    :exclude-members: BASE_URL

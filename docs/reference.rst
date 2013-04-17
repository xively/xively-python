=============
API Reference
=============

.. module:: cosm

The cosm-python library consists of two layers. The top layer uses the
:class:`CosmAPIClient` and object wrappers.  The lower layer via
:class:`Client` gives access directly to sending native python types and
accessing the response.

API Client
==========

.. autoclass:: cosm.CosmAPIClient
    :members:
    :undoc-members:

Feeds, Datastreams and Datapoints
---------------------------------

.. autoclass:: cosm.api.FeedsManager
    :members:
    :undoc-members:

.. autoclass:: cosm.Feed
    :members:
    :undoc-members:

.. autoclass:: cosm.api.DatastreamsManager
    :members:
    :undoc-members:
    :exclude-members: resource

.. autoclass:: cosm.Datastream
    :members:
    :undoc-members:

.. autoclass:: cosm.api.DatapointsManager
    :members:
    :undoc-members:

.. autoclass:: cosm.Datapoint
    :members:
    :undoc-members:

Location and Waypoints
----------------------

.. autoclass:: cosm.Location
    :members:
    :undoc-members:

.. autoclass:: cosm.Waypoint
    :members:
    :undoc-members:

API Keys
--------

.. autoclass:: cosm.api.KeysManager
    :members:
    :undoc-members:

.. autoclass:: cosm.Key
    :members:
    :undoc-members:

.. autoclass:: cosm.Permission
    :members:
    :undoc-members:

.. autoclass:: cosm.Resource
    :members:
    :undoc-members:

Triggers
--------

.. autoclass:: cosm.api.TriggersManager
    :members:
    :undoc-members:

.. autoclass:: cosm.Trigger
    :members:
    :undoc-members:

Low Level Client
================

.. autoclass:: cosm.Client
    :members:
    :undoc-members:
    :show-inheritance:

# -*- coding: utf-8 -*-

__title__ = 'cosm-python'
__version__ = '0.1.0'

__all__ = ['CosmApiClient', 'Client', 'Feed', 'Datastream', 'Datapoint',
           'Location', 'Waypoint', 'Trigger', 'Key', 'Permission', 'Resource']

from cosm.api import CosmAPIClient
from cosm.client import Client
from cosm.models import (
    Feed, Datastream, Datapoint, Location, Waypoint, Trigger, Key, Permission,
    Resource)


def setup_module(module):
    import mock
    import fixtures
    patcher = mock.patch('cosm.client.Session.request')
    mock_request = patcher.start()
    mock_request.side_effect = fixtures.handle_request
    module._patcher = patcher


def teardown_module(module):
    module._patcher.stop()


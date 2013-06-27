# -*- coding: utf-8 -*-

__title__ = 'xively-python'
__version__ = '0.1.0-rc2'

__all__ = ['Client', 'XivelyAPIClient', 'Datapoint', 'Datastream', 'Feed', 'Key',
           'Location', 'Permission', 'Resource', 'Trigger', 'Unit', 'Waypoint']

from xively.api import XivelyAPIClient
from xively.client import Client
from xively.models import (
    Datapoint, Datastream, Feed, Key, Location, Permission, Resource, Trigger,
    Unit, Waypoint)


def setup_module(module):
    import mock
    import fixtures
    patcher = mock.patch('xively.client.Session.request')
    mock_request = patcher.start()
    mock_request.side_effect = fixtures.handle_request
    module._patcher = patcher


def teardown_module(module):
    module._patcher.stop()

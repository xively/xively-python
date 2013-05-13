# -*- coding: utf-8 -*-

import mock
import requests

try:
    from io import BytesIO
except TypeError:
    from StringIO import StringIO as BytesIO  # NOQA

import xively
import fixtures


def setup_module(module):
    patcher = mock.patch('xively.client.Session.request')
    mock_request = patcher.start()
    mock_request.side_effect = handle_request
    module._patcher = patcher


def teardown_module(module):
    module._patcher.stop()


responses_by_url = {
    'feeds/7021': fixtures.GET_FEED_JSON,
    'feeds/7021/datastreams/3': fixtures.HISTORY_DATASTREAM_JSON,
}


def handle_request(method, url, *args, **kwargs):
    response = requests.Response()
    response.status_code = 200
    relative_url = url.replace("http://api.xively.com/v2/", '')
    if relative_url in responses_by_url:
        response.raw = BytesIO(responses_by_url[relative_url])
    return response

# -*- coding: utf-8 -*-

import unittest

import requests

from mock import Mock, patch

import cosm


class RequestsFixtureMixin(object):
    """Mixin to mock request.Session.request from the cosm module."""

    def setUp(self, *args, **kwargs):
        """Installs our own request handler."""
        patcher = patch('cosm.Session.request')
        self.session = patcher.start()
    setUp.__test__ = False  # Don't test this method.

    def tearDown(self, *args, **kwargs):
        """Ensures the original request object is reinstated."""
        self.session.stop()
    tearDown.__test__ = False  # Don't test this method.

    def request(self, *args, **kwargs):
        """Returns a new mock object by default. Override in implementors."""
        return Mock()


class BaseTestCase(RequestsFixtureMixin, unittest.TestCase):
    pass


class KeyAuthTest(unittest.TestCase):

    def test_api_key_header(self):
        request = requests.Request()
        auth = cosm.KeyAuth("ABCDE")
        auth(request)
        self.assertEqual(request.headers['X-ApiKey'], "ABCDE")


class ClientTest(BaseTestCase):

    def test_create(self):
        """Tests that we can create a client object."""
        cosm.Client("ABCDE")

    def test_request_relative_url(self):
        """Tests relative urls are requested with absolute url."""
        client = cosm.Client("API_KEY")
        client.request('GET', "/v2/feeds")
        self.session.assert_called_with('GET', "http://api.cosm.com/v2/feeds")

    def test_request_absolute_url(self):
        """Tests absolute urls are requested for a different host."""
        client = cosm.Client("API_KEY")
        client.request('GET', "http://example.com")
        self.session.assert_called_with('GET', "http://example.com")

    def test_serialise_data(self):
        """Tests data is serialised using __getstate__ when requested."""
        class TestObject:
            def __getstate__(self):
                return self.__dict__
        obj = TestObject()
        obj.title = "This is an object"
        obj.value = 42
        client = cosm.Client("API_KEY")
        client.request('POST', "/v2/feeds", data=obj)
        self.session.assert_called_with(
            'POST', "http://api.cosm.com/v2/feeds",
            data={'title': "This is an object", "value": 42})


class FeedTest(BaseTestCase):

    def setUp(self):
        super(FeedTest, self).setUp()
        self.client = cosm.Client("API_KEY")

    def test_create_feed(self):
        feed = cosm.Feed(title="Feed Test")
        self.client.post('/v2/feeds', data=feed)

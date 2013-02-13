# -*- coding: utf-8 -*-

import unittest

from mock import Mock, patch

import cosm


class RequestsFixtureMixin(object):
    """Mixin to mock request.Session.request from the cosm module."""

    def setUp(self, *args, **kwargs):
        """Installs our own request handler."""
        patcher = patch('cosm.Session.request')
        self.session = patcher.start()
        self.session.side_effect = self.request
    setUp.__test__ = False  # Don't test this method.

    def tearDown(self, *args, **kwargs):
        """Ensures the original request object is reinstated."""
        self.session.stop()
    tearDown.__test__ = False  # Don't test this method.

    def request(self, *args, **kwargs):
        """Returns a new mock object by default. Override in implementors."""
        return Mock()


class ClientTest(RequestsFixtureMixin, unittest.TestCase):

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

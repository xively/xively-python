# -*- coding: utf-8 -*-

import StringIO
import json
import unittest

import requests

from mock import Mock, patch

import cosm
import cosm.api


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
    """Common base class for Cosm api tests."""
    pass


class KeyAuthTest(unittest.TestCase):
    """
    Key based authentication tests.
    """

    def test_api_key_header(self):
        """Tests the X-ApiKey header is set on requests using KeyAuth."""
        request = requests.Request()
        auth = cosm.KeyAuth("ABCDE")
        auth(request)
        self.assertEqual(request.headers['X-ApiKey'], "ABCDE")


class ClientTest(BaseTestCase):
    """
    Low level Cosm Client tests.
    """

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


class APIClientTest(BaseTestCase):
    """
    Cosm API Client tests.
    """

    def setUp(self):
        super(APIClientTest, self).setUp()
        self.client = cosm.api.Client("API_KEY")

    def test_create_feed(self):
        """Tests a request is sent to create a feed and return a location."""
        response = requests.Response()
        response.status_code = 201
        response.headers['location'] = "http://cosm.api.com/v2/feeds/51"
        with patch('cosm.Session.request') as request:
            request.return_value = response
            location = self.client.feeds.create(title="Area 51")
        self.assertEqual(location, "http://cosm.api.com/v2/feeds/51")

    def test_update_feed(self):
        """Tests a request is sent to update a feed by its id."""
        response = requests.Response()
        response.status_code = 200
        self.session.return_value = response
        self.client.feeds.update(51, private=True)
        self.session.assert_called_with(
            'PUT', 'http://api.cosm.com/v2/feeds/51',
            data='{"private": true}')

    def test_list_feeds(self):
        """Tests a request is sent to list all feeds and return as json."""
        response = requests.Response()
        response.status_code = 200
        response.raw = StringIO.StringIO('{"totalResults": 0, "results": []}')
        self.session.return_value = response
        result = self.client.feeds.list()
        self.assertEqual(self.session.call_args[0],
                         ('GET', 'http://api.cosm.com/v2/feeds.json'))
        self.assertEqual(result['results'], [])

    def test_view_feed(self):
        """Tests a request is sent to view a feed (by id) returning json."""
        response = requests.Response()
        response.status_code = 200
        response.raw = StringIO.StringIO(FEED_JSON)
        self.session.return_value = response
        result = self.client.feeds.get(7021)
        self.assertEqual(self.session.call_args[0],
                         ('GET', 'http://api.cosm.com/v2/feeds/7021.json'))
        self.assertEqual(result, json.loads(FEED_JSON))

    def test_delete_feed(self):
        """Tests a DELETE request is sent for a feed by its id."""
        response = requests.Response()
        response.status_code = 200
        self.session.return_response = response
        self.client.feeds.delete(7021)
        self.session.assert_called_with(
            'DELETE', 'http://api.cosm.com/v2/feeds/7021')


# Data used to return in the responses.

FEED_JSON = '''
{
"description" : "test of manual feed snapshotting",
"feed" : "http://api.cosm.com/v2/feeds/504.json",
"id" : 7021,
"status" : "frozen",
"title" : "Cosm Office environment",
"website":"http://www.haque.co.uk/",
"updated" : "2010-06-25T11:54:17.463771Z",
"created" : "2010-05-03T23:43:01.238734Z",
"version" : "1.0.0",
"creator" : "https://cosm.com/users/hdr",
"tags":[
    "Tag1",
    "Tag2"
],
"location":
{
  "disposition":"fixed",
  "ele":"23.0",
  "name":"office",
  "lat":51.5235375648154,
  "exposure":"indoor",
  "lon":-0.0807666778564453,
  "domain":"physical"
},
"datastreams" : [ {
  "at" : "2010-06-25T11:54:17.454020Z",
  "current_value" : "999",
  "id" : "3",
  "max_value" : "999.0",
  "min_value" : "7.0"
  },
  {
  "at" : "2010-06-24T10:05:49.000000Z",
  "current_value" : "0000017",
  "id" : "4",
  "max_value" : "19.0",
  "min_value" : "7.0"
  } ]
}
'''

# -*- coding: utf-8 -*-

"""
A Fixture class specifically for mocking requests for the README doctests.

requests.Session.request is mocked out and a request.Response returned
dependant on the given arguments to request.

"""

from mock import patch
from requests import Response


class Fixture(object):
    """A class to hold the mock request object and not pollute globals."""

    def setup_test(self, test):
        """Installs our own request handler."""
        patcher = patch('cosm.Session.request')
        self.mock_session = patcher.start()
        self.mock_session.side_effect = self.request
    setup_test.__test__ = False  # Don't test this method.

    def teardown_test(self, test):
        """Ensures the original request object is reinstated."""
        self.mock_session.stop()
    teardown_test.__test__ = False  # Don't test this method.

    def request(self, method, url, **kwargs):
        """
        Returns a Response object that we would expect return from Cosm.

        We don't want to actually hit Cosm's API during our tests so instead we
        intercept requests and return the responses that we would expect
        depending on what arguments we were given.
        """
        response = Response()
        response.status_code = 200
        if url == 'http://api.cosm.com/v2/feeds.json':
            response.headers['Location'] = 'http://api.cosm.com/v2/feeds/504'
        return response

# setup_test and teardown_test must live at the module level to be discovered.
_fixture = Fixture()
setup_test = _fixture.setup_test
teardown_test = _fixture.teardown_test

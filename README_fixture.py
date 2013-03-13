# -*- coding: utf-8 -*-

"""
A Fixture class specifically for mocking requests for the README doctests.

requests.Session.request is mocked out and a request.Response returned
dependant on the given arguments to request.

"""

from requests import Response

from tests import RequestsFixtureMixin


class Fixture(RequestsFixtureMixin):
    """A class to hold the mock request object and not pollute globals."""

    def setUp(self, *args, **kwargs):
        super(Fixture, self).setUp()
        self.request.side_effect = self.handle_request

    def handle_request(self, method, url, **kwargs):
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
setup_test = _fixture.setUp
teardown_test = _fixture.tearDown

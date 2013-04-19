# -*- coding: utf-8 -*-

"""
A Fixture class specifically for mocking requests for the README doctests.

requests.Session.request is mocked out and a request.Response returned
dependant on the given arguments to request.

"""

from requests import Response

from tests import RequestsFixtureMixin

import fixtures

class Fixture(RequestsFixtureMixin):
    """A class to hold the mock request object and not pollute globals."""

    def setUp(self, *args, **kwargs):
        super(Fixture, self).setUp()
        self.request.side_effect = fixtures.handle_request


# setup_test and teardown_test must live at the module level to be discovered.
_fixture = Fixture()
setup_test = _fixture.setUp
teardown_test = _fixture.tearDown

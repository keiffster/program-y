import unittest

from programy.clients.restful.auth import RestBasicAuthorizationHandler
from programy.clients.restful.config import RestConfiguration


class MockRestBasicAuthorizationHandler(RestBasicAuthorizationHandler):

    def __init__(self, configuration: RestConfiguration):
        RestBasicAuthorizationHandler.__init__(self, configuration)
        self.auth_token = None

    def get_license_key(self):
        return self.auth_token


class MockRequest(object):

    def __init__(self):
        self.headers = {}


class RestBasicAuthorizationHandlerTests(unittest.TestCase):

    def test_init(self):
        config = RestConfiguration("test")
        self.assertIsNotNone(config)

        handler = MockRestBasicAuthorizationHandler(config)
        self.assertIsNotNone(handler)
        handler.auth_token = "1234567890"

        handler.initialise(None)
        self.assertEquals("1234567890", handler._basic_auth_token)

    def test_authorise_valid_header(self):
        config = RestConfiguration("test")
        self.assertIsNotNone(config)

        handler = MockRestBasicAuthorizationHandler(config)
        self.assertIsNotNone(handler)
        handler.auth_token = "1234567890"

        handler.initialise(None)

        request = MockRequest()
        request.headers['AUTHORISATION'] = 'Basic 1234567890'

        self.assertTrue(handler.authorise(request))

    def test_authorise_invalid_header(self):
        config = RestConfiguration("test")
        self.assertIsNotNone(config)

        handler = MockRestBasicAuthorizationHandler(config)
        self.assertIsNotNone(handler)
        handler.auth_token = "1234567890"

        handler.initialise(None)

        request = MockRequest()
        request.headers['AUTHORISATION'] = 'Basic 0123456789'

        self.assertFalse(handler.authorise(request))

    def test_authorise_noheader(self):
        config = RestConfiguration("test")
        self.assertIsNotNone(config)

        handler = MockRestBasicAuthorizationHandler(config)
        self.assertIsNotNone(handler)
        handler.auth_token = "1234567890"

        handler.initialise(None)

        request = MockRequest()

        self.assertFalse(handler.authorise(request))

import unittest

from programy.clients.restful.auth import RestBasicAuthorizationHandler
from programy.clients.restful.auth import RestAuthorizationHandler
from programy.clients.restful.client import RestBotClient
from programy.clients.restful.config import RestConfiguration

from programytest.clients.arguments import MockArgumentParser


class MockRestBasicAuthorizationHandler(RestBasicAuthorizationHandler):

    def __init__(self, configuration: RestConfiguration):
        RestBasicAuthorizationHandler.__init__(self, configuration)
        self.auth_token = None

    def get_license_key(self):
        return self.auth_token


class MockRequest(object):

    def __init__(self):
        self.headers = {}


class RestAuthorizationHandlerTests(unittest.TestCase):

    def test_basic_authorisation(self):

        arguments = MockArgumentParser()
        client = RestBotClient("testrest", arguments)
        self.assertIsNotNone(client)

        client.license_keys.add_key('BASIC_AUTH_TOKEN', "1234567890")
        client.configuration.client_configuration._authorization = "Basic"

        handler = RestAuthorizationHandler.load_authorisation(client)
        self.assertIsNotNone(handler)

    def test_unsupported_authorisation(self):

        arguments = MockArgumentParser()
        client = RestBotClient("testrest", arguments)
        self.assertIsNotNone(client)

        client.configuration.client_configuration._authorization = "Sha"

        handler = RestAuthorizationHandler.load_authorisation(client)
        self.assertIsNone(handler)


class RestBasicAuthorizationHandlerTests(unittest.TestCase):

    def test_init(self):
        config = RestConfiguration("test")
        self.assertIsNotNone(config)

        handler = MockRestBasicAuthorizationHandler(config)
        self.assertIsNotNone(handler)
        handler.auth_token = "1234567890"

        arguments = MockArgumentParser()
        client = RestBotClient("testrest", arguments)
        self.assertIsNotNone(client)
        client.license_keys.add_key('BASIC_AUTH_TOKEN', "1234567890")

        handler.initialise(client)
        self.assertEquals("1234567890", handler._basic_auth_token)

    def test_authorise_valid_header(self):
        config = RestConfiguration("test")
        self.assertIsNotNone(config)

        handler = MockRestBasicAuthorizationHandler(config)
        self.assertIsNotNone(handler)
        handler.auth_token = "1234567890"

        arguments = MockArgumentParser()
        client = RestBotClient("testrest", arguments)
        self.assertIsNotNone(client)
        client.license_keys.add_key('BASIC_AUTH_TOKEN', "1234567890")

        handler.initialise(client)

        request = MockRequest()
        request.headers['Authorization'] = 'Basic 1234567890'

        self.assertTrue(handler.authorise(request))

    def test_authorise_invalid_header(self):
        config = RestConfiguration("test")
        self.assertIsNotNone(config)

        handler = MockRestBasicAuthorizationHandler(config)
        self.assertIsNotNone(handler)
        handler.auth_token = "1234567890"

        arguments = MockArgumentParser()
        client = RestBotClient("testrest", arguments)
        self.assertIsNotNone(client)
        client.license_keys.add_key('BASIC_AUTH_TOKEN', "1234567890")

        handler.initialise(client)

        request = MockRequest()
        request.headers['AUTHORISATION'] = 'Basic 0123456789'

        self.assertFalse(handler.authorise(request))

    def test_authorise_noheader(self):
        config = RestConfiguration("test")
        self.assertIsNotNone(config)

        handler = MockRestBasicAuthorizationHandler(config)
        self.assertIsNotNone(handler)
        handler.auth_token = "1234567890"

        arguments = MockArgumentParser()
        client = RestBotClient("testrest", arguments)
        self.assertIsNotNone(client)
        client.license_keys.add_key('BASIC_AUTH_TOKEN', "1234567890")

        handler.initialise(client)

        request = MockRequest()

        self.assertFalse(handler.authorise(request))

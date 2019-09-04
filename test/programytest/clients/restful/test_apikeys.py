import unittest
import os

from programy.clients.restful.apikeys import APIKeysHandler
from programy.clients.restful.client import RestBotClient
from programy.clients.restful.config import RestConfiguration

from programytest.clients.arguments import MockArgumentParser


class MockRequest(object):

    def __init__(self):
        self.args = {}


class APIKeysHandlerTests(unittest.TestCase):

    def test_init(self):
        config = RestConfiguration("test")
        self.assertIsNotNone(config)

        handler = APIKeysHandler(config)
        self.assertIsNotNone(handler)

        self.assertFalse(handler.use_api_keys())

    def test_api_keys(self):
        arguments = MockArgumentParser()
        client = RestBotClient("testrest", arguments)
        self.assertIsNotNone(client)

        client.configuration.client_configuration._use_api_keys = True
        client.configuration.client_configuration._api_key_file = os.path.dirname(__file__) + os.sep + ".." + os.sep + "api_keys.txt"

        client.initialise()

        self.assertEqual(3, len(client.api_keys.api_keys))
        self.assertTrue(client.api_keys.is_apikey_valid("11111111"))
        self.assertTrue(client.api_keys.is_apikey_valid("22222222"))
        self.assertTrue(client.api_keys.is_apikey_valid("33333333"))
        self.assertFalse(client.api_keys.is_apikey_valid("99999999"))

    def test_get_api_key(self):
        config = RestConfiguration("test")
        self.assertIsNotNone(config)

        handler = APIKeysHandler(config)
        self.assertIsNotNone(handler)

        request = MockRequest()
        request.args['apikey'] = '11111111'

        self.assertEquals('11111111', handler.get_api_key(request))

    def test_verify_api_key_usage(self):
        arguments = MockArgumentParser()
        client = RestBotClient("testrest", arguments)
        self.assertIsNotNone(client)

        client.configuration.client_configuration._use_api_keys = True
        client.configuration.client_configuration._api_key_file = os.path.dirname(__file__) + os.sep + ".." + os.sep + "api_keys.txt"

        client.initialise()

        request = MockRequest()
        request.args['apikey'] = '11111111'

        self.assertTrue(client.api_keys.verify_api_key_usage(request))

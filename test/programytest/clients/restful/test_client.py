import unittest
import unittest.mock
import os

from programy.clients.restful.client import RestBotClient
from programy.clients.restful.config import RestConfiguration

from programytest.clients.arguments import MockArgumentParser


class RestBotClientTests(unittest.TestCase):

    def test_init(self):
        arguments = MockArgumentParser()
        client = RestBotClient("testrest", arguments)
        self.assertIsNotNone(client)
        self.assertIsNotNone(client.get_client_configuration())
        self.assertIsInstance(client.get_client_configuration(), RestConfiguration)
        self.assertEqual([], client.api_keys.api_keys)

        request = unittest.mock.Mock()
        response, code = client.process_request(request, version=1.0)
        self.assertIsNotNone(response)
        self.assertIsNotNone(code)
        self.assertEquals(500, code)

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
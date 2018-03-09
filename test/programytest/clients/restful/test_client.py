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
        self.assertEquals([], client.api_keys)

        request = unittest.mock.Mock()
        response, code = client.process_request(request)

    def test_api_keys(self):
        arguments = MockArgumentParser()
        client = RestBotClient("testrest", arguments)
        self.assertIsNotNone(client)

        client.configuration.client_configuration._use_api_keys = True
        client.configuration.client_configuration._api_key_file = os.path.dirname(__file__) + os.sep + ".." + os.sep + "api_keys.txt"

        client.load_api_keys()

        self.assertEquals(3, len(client.api_keys))
        self.assertTrue(client.is_apikey_valid("11111111"))
        self.assertTrue(client.is_apikey_valid("22222222"))
        self.assertTrue(client.is_apikey_valid("33333333"))
        self.assertFalse(client.is_apikey_valid("99999999"))
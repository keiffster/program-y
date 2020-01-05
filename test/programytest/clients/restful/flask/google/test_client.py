import unittest.mock

from programy.clients.restful.flask.google.client import GoogleBotClient
from programy.clients.restful.flask.google.config import GoogleConfiguration
from programy.clients.render.text import TextRenderer
from programytest.clients.arguments import MockArgumentParser


class MockGoogleBotClient(GoogleBotClient):

    def test__init__(self, argument_parser=None):
        GoogleBotClient.__init__(self, argument_parser)

    def _to_json(self, data):
        return data


class MockHttpRequest(object):

    def __init__(self, data):
        self.data = data


class GoogleClientBotClientTests(unittest.TestCase):

    def test_google_client_init(self):
        arguments = MockArgumentParser()
        client = MockGoogleBotClient(arguments)
        self.assertIsNotNone(client)

        self.assertIsInstance(client.get_client_configuration(), GoogleConfiguration)
        self.assertEqual('ProgramY AIML2.0 Client', client.get_description())

        self.assertFalse(client._render_callback())
        self.assertIsInstance(client.renderer, TextRenderer)

    def test_client_configuration(self):
        arguments = MockArgumentParser()
        client = MockGoogleBotClient(arguments)
        self.assertIsNotNone(client)
        config = client.get_client_configuration()
        self.assertIsNotNone(config)
        self.assertIsInstance(config, GoogleConfiguration)

    def test_receive_launch_intent_message(self):
        arguments = MockArgumentParser()
        client = MockGoogleBotClient(arguments)
        self.assertIsNotNone(client)

        http_request = MockHttpRequest("""
        {
            "queryResult": {
              "intent": {
                "displayName": "Launch Intent"
              },
              "session": "test session"
            }
        }
        """
                                       )
        client.receive_message(http_request)

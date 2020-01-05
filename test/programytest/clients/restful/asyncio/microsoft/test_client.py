"""
import unittest

from programytest.clients.arguments import MockArgumentParser
from programy.clients.restful.asyncio.microsoft.client import MicrosoftBotClient
from programy.clients.restful.asyncio.microsoft.config import MicrosoftConfiguration

from programy.clients.render.text import TextRenderer


class MockMicrosoftBotClient(MicrosoftBotClient):

    def __init__(self, arguements):
        MicrosoftBotClient.__init__(self, arguements)


class MicrosoftBotClientTests(unittest.TestCase):

    def test_init(self):
        arguments = MockArgumentParser()

        client = MockMicrosoftBotClient(arguments)
        self.assertIsNotNone(client)
        self.assertIsNotNone(client.arguments)
        self.assertEqual(client.id, "microsoft")
        self.assertEqual('ProgramY AIML2.0 Client', client.get_description())
        self.assertIsInstance(client.get_client_configuration(), MicrosoftConfiguration)

        self.assertFalse(client._render_callback())
        self.assertIsInstance(client.renderer, TextRenderer)
"""

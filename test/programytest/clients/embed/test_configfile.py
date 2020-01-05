import unittest

from programy.clients.config import ClientConfigurationData
from programy.clients.embed.configfile import EmbeddedConfigFileBot
from programytest.clients.arguments import MockArgumentParser
from programy.clients.render.text import TextRenderer


class EmbeddedBotClientTests(unittest.TestCase):

    def test_init(self):
        arguments = MockArgumentParser()
        client = EmbeddedConfigFileBot(arguments)
        self.assertIsNotNone(client)

        self.assertEqual('ProgramY AIML2.0 Client', client.get_description())
        self.assertIsInstance(client.get_client_configuration(), ClientConfigurationData)

        self.assertFalse(client._render_callback())
        self.assertIsInstance(client.renderer, TextRenderer)

        client_context = client.create_client_context("testuser")
        self.assertEqual("", client_context.bot.ask_question(client_context, "Hello"))

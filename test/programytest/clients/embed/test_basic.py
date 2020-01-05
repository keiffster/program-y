import unittest

from programy.clients.config import ClientConfigurationData
from programy.clients.embed.basic import EmbeddedBasicBot
from programy.clients.render.text import TextRenderer


class EmbeddedBasicBotClientTests(unittest.TestCase):

    def test_init(self):
        client = EmbeddedBasicBot()
        self.assertIsNotNone(client)

        self.assertEqual('ProgramY AIML2.0 Client', client.get_description())
        self.assertIsInstance(client.get_client_configuration(), ClientConfigurationData)

        self.assertFalse(client._render_callback())
        self.assertIsInstance(client.renderer, TextRenderer)

        self.assertNotEqual("", client.ask_question("Hello"))



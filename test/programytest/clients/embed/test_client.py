import unittest

from programy.clients.embed.client import MyEmbeddedBot
from programy.clients.config import ClientConfigurationData

from programytest.clients.arguments import MockArgumentParser


class EmbeddedBotClientTests(unittest.TestCase):

    def test_init(self):
        arguments = MockArgumentParser()
        client = MyEmbeddedBot(arguments)
        self.assertIsNotNone(client)
        self.assertEqual('ProgramY AIML2.0 Client', client.get_description())
        self.assertIsInstance(client.get_client_configuration(), ClientConfigurationData)

import unittest

from programy.clients.console import ConsoleBotClient

from test.clients.arguments import MockArgumentParser

class ConsoleBotClientTests(unittest.TestCase):

    def test_console_client(self):
        arguments = MockArgumentParser()
        client = ConsoleBotClient(arguments)
        self.assertIsNotNone(client)


import unittest

from programy.clients.rest2 import RestBotClient

from test.clients.arguments import MockArgumentParser

class Rest2BotClientTests(unittest.TestCase):

    def test_rest_client(self):
        arguments = MockArgumentParser()
        client = RestBotClient(arguments)
        self.assertIsNotNone(client)


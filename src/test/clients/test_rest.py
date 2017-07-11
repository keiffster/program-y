import unittest

from programy.clients.rest import RestBotClient

from test.clients.arguments import MockArgumentParser

class RestBotClientTests(unittest.TestCase):

    def test_rest_client(self):
        arguments = MockArgumentParser()
        client = RestBotClient(arguments)
        self.assertIsNotNone(client)


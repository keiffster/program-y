import unittest

from programy.clients.xmpp import XmppBotClient

from test.clients.arguments import MockArgumentParser

class ConsoleBotClientTests(unittest.TestCase):

    def test_xmpp_client(self):
        arguments = MockArgumentParser()
        client = XmppBotClient(arguments)
        self.assertIsNotNone(client)


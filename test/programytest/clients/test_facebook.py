"""
import unittest

from programy.clients.facebook import FacebookBotClient

from programytest.clients.arguments import MockArgumentParser

class FacebookBotClientTests(unittest.TestCase):

    def test_facebook_client(self):
        arguments = MockArgumentParser()
        client = FacebookBotClient(arguments)
        self.assertIsNotNone(client)

"""
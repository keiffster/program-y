import unittest

from programy.clients.twitter import TwitterBotClient

from test.clients.arguments import MockArgumentParser

class TwitterBotClientTests(unittest.TestCase):

    def test_twitter_client(self):
        arguments = MockArgumentParser()
        client = TwitterBotClient(arguments)
        self.assertIsNotNone(client)


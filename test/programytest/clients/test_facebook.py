import unittest
import unittest.mock
import os
from pymessenger.bot import Bot

from programy.clients.facebook import FacebookBotClient
from programy.config.sections.client.facebook import FacebookConfiguration

from programytest.clients.arguments import MockArgumentParser

class TestFacebookBotClient(FacebookBotClient):

    def __init__(self, argument_parser=None, facebook_bot=None):
        self.test_facebook_bot = facebook_bot
        self.test_question = None
        FacebookBotClient.__init__(self, argument_parser)

    def set_question(self, question):
        self.test_question = question

    def get_license_keys(self):
        self.access_token = "FACEBOOK_ACCESS_TOKEN"
        self.verify_token = "FACEBOOK_VERIFY_TOKEN"

    def ask_question(self, sessionid, question):
        if self.test_question is not None:
            return self.test_question
        return super(TestFacebookBotClient, self).ask_question(sessionid, question)

    def create_facebook_bot(self):
        if self.test_facebook_bot is not None:
            return self.test_facebook_bot
        return super(TestFacebookBotClient,self).create_facebook_bot()

class RestBotClientTests(unittest.TestCase):

    def test_rest_client_init(self):
        arguments = MockArgumentParser()
        client = TestFacebookBotClient(arguments)
        self.assertIsNotNone(client)

        self.assertEquals("FACEBOOK_VERIFY_TOKEN", client.verify_token)
        self.assertEquals("FACEBOOK_ACCESS_TOKEN", client.access_token)

        self.assertEquals("Facebook", client.bot.brain.properties.property("env"))

        self.assertIsInstance(client.get_client_configuration(), FacebookConfiguration)

        self.assertIsInstance(client.facebook_bot, Bot)
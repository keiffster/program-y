import unittest
import unittest.mock
import os
from pymessenger.bot import Bot

from programy.clients.twilio import TwilioBotClient
from programy.config.sections.client.twilio import TwilioConfiguration

from programytest.clients.arguments import MockArgumentParser

class TestTwilioBotClient(TwilioBotClient):

    def __init__(self, argument_parser=None, twilio_client=None):
        self.test_twilio_client = twilio_client
        self.test_question = None
        TwilioBotClient.__init__(self, argument_parser)

    def set_question(self, question):
        self.test_question = question

    def get_license_keys(self):
        self._access_token = "TWILIO_ACCESS_TOKEN"
        self._verify_token = "TWILIO_VERIFY_TOKEN"
        self._from_number  = "+447777777777"

    def ask_question(self, sessionid, question):
        if self.test_question is not None:
            return self.test_question
        return super(TestTwilioBotClient, self).ask_question(sessionid, question)

    def create_twilio_client(self):
        if self.test_twilio_client is not None:
            return self.test_twilio_client
        return super(TestTwilioBotClient,self).create_twilio_client()

class TwilioBotClientTests(unittest.TestCase):

    def test_twilio_client_init(self):
        arguments = MockArgumentParser()
        client = TestTwilioBotClient(arguments)
        self.assertIsNotNone(client)

        self.assertEquals("TWILIO_VERIFY_TOKEN", client._verify_token)
        self.assertEquals("TWILIO_ACCESS_TOKEN", client._access_token)
        self.assertEquals("+447777777777", client._from_number)

        self.assertEquals("Twilio", client.bot.brain.properties.property("env"))

        self.assertIsInstance(client.get_client_configuration(), TwilioConfiguration)

        self.assertIsInstance(client.twilio_client, Bot)
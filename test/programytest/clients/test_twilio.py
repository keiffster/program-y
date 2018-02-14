import unittest.mock

from twilio.rest import Client

from programy.clients.twilio_client import TwilioBotClient
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
        self._account_sid = "TWILIO_ACCOUNT_SID"
        self._auth_token = "TWILIO_AUTH_TOKEN"
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

        self.assertEquals("TWILIO_ACCOUNT_SID", client._account_sid)
        self.assertEquals("TWILIO_AUTH_TOKEN", client._auth_token)
        self.assertEquals("+447777777777", client._from_number)

        self.assertEquals("Twilio", client.bot.brain.properties.property("env"))

        self.assertIsInstance(client.get_client_configuration(), TwilioConfiguration)

        self.assertIsInstance(client._twilio_client, Client)
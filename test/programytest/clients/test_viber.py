import unittest.mock
import logging

from viberbot import Api

from programy.clients.viber_client import ViberBotClient
from programy.config.sections.client.viber_client import ViberConfiguration

from programytest.clients.arguments import MockArgumentParser


class MockViberApi(Api):

    def __init__(self, bot_configuration):
        pass

    def set_webhook(self, url, webhook_events=None, is_inline=False):
        pass

class TestViberBotClient(ViberBotClient):

    def __init__(self, argument_parser=None, viber_client=None):
        self.test_viber_client = viber_client
        self.test_question = None
        ViberBotClient.__init__(self, argument_parser)

    def set_question(self, question):
        self.test_question = question

    def get_token(self, license_keys):
        return "VIBER_TOKEN"

    def ask_question(self, sessionid, question):
        if self.test_question is not None:
            return self.test_question
        return super(TestViberBotClient, self).ask_question(sessionid, question)

    def create_viber_api(self, bot_configuration):
        return MockViberApi(bot_configuration)

    def create_viber_bot(self, viber_token):
        if self.test_viber_client is not None:
            return self.test_viber_client
        return super(TestViberBotClient,self).create_viber_bot(viber_token)


class ViberBotClientTests(unittest.TestCase):

    def test_viber_client_init(self):
        arguments = MockArgumentParser()
        client = TestViberBotClient(arguments)
        self.assertIsNotNone(client)

        self.assertEquals("VIBER_TOKEN", client._viber_token)
        self.assertIsNotNone(client._viber_bot)
        self.assertEquals("viber", client.bot.brain.properties.property("env"))

        self.assertIsInstance(client.get_client_configuration(), ViberConfiguration)

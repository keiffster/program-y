import unittest.mock

from kik import KikApi

from programy.clients.kik_client import KikBotClient
from programy.config.sections.client.kik_client import KikConfiguration

from programytest.clients.arguments import MockArgumentParser

class MockKikApi(KikApi):

    def __init__(self, bot, api_key):
        pass

class TestKikBotClient(KikBotClient):

    def __init__(self, argument_parser=None, kik_client=None):
        self.test_kik_client = kik_client
        self.test_question = None
        KikBotClient.__init__(self, argument_parser)

    def set_question(self, question):
        self.test_question = question

    def get_tokens(self):
        self._bot_api_key = "KIK_BOT_API_KEY"

    def ask_question(self, sessionid, question):
        if self.test_question is not None:
            return self.test_question
        return super(TestKikBotClient, self).ask_question(sessionid, question)

    def create_kik_bot(self):
        if self.test_kik_client is not None:
            return self.test_kik_client
        return super(TestKikBotClient,self).create_kik_bot()


class KikBotClientTests(unittest.TestCase):

    def test_kik_client_init(self):
        arguments = MockArgumentParser()
        client = TestKikBotClient(arguments, kik_client=MockKikApi(bot="test", api_key=None))
        self.assertIsNotNone(client)

        self.assertEquals("KIK_BOT_API_KEY", client._bot_api_key)

        self.assertEquals("kik", client.bot.brain.properties.property("env"))

        self.assertIsInstance(client.get_client_configuration(), KikConfiguration)


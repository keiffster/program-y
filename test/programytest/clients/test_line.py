import unittest.mock

from programy.clients.line_client import LineBotClient
from programy.config.sections.client.line_client import LineConfiguration

from programytest.clients.arguments import MockArgumentParser

class TestLineBotClient(LineBotClient):

    def __init__(self, argument_parser=None, line_client=None):
        self.test_line_client = line_client
        self.test_question = None
        LineBotClient.__init__(self, argument_parser)

    def set_question(self, question):
        self.test_question = question

    def get_tokens(self):
        self._channel_secret = "LINE_CHANNEL_SECRET"
        self._channel_access_token = "LINE_ACCESS_TOKEN"

    def ask_question(self, sessionid, question):
        if self.test_question is not None:
            return self.test_question
        return super(TestLineBotClient, self).ask_question(sessionid, question)

    def create_line_bot(self):
        if self.test_line_client is not None:
            return self.test_line_client
        return super(TestLineBotClient,self).create_line_bot()


class LineBotClientTests(unittest.TestCase):

    def test_line_client_init(self):
        arguments = MockArgumentParser()
        client = TestLineBotClient(arguments)
        self.assertIsNotNone(client)

        self.assertEquals("LINE_CHANNEL_SECRET", client._channel_secret)
        self.assertEquals("LINE_ACCESS_TOKEN", client._channel_access_token)

        self.assertEquals("line", client.bot.brain.properties.property("env"))

        self.assertIsInstance(client.get_client_configuration(), LineConfiguration)


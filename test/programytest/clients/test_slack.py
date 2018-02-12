import unittest.mock

from slackclient import SlackClient

from programy.clients.slack_client import SlackBotClient
from programy.config.sections.client.slack_client import SlackConfiguration

from programytest.clients.arguments import MockArgumentParser

class TestSlackBotClient(SlackBotClient):

    def __init__(self, argument_parser=None, slack_client=None):
        self.test_slack_client = slack_client
        self.test_question = None
        SlackBotClient.__init__(self, argument_parser)

    def set_question(self, question):
        self.test_question = question

    def get_token(self,):
         self._bot_token = "SLACK_BOT_TOKEN"

    def ask_question(self, sessionid, question):
        if self.test_question is not None:
            return self.test_question
        return super(TestSlackBotClient, self).ask_question(sessionid, question)

    def create_slack_client(self):
        if self.test_slack_client is not None:
            return self.test_slack_client
        return super(TestSlackBotClient,self).create_slack_client()

class SlackBotClientTests(unittest.TestCase):

    def test_slack_client_init(self):
        arguments = MockArgumentParser()
        client = TestSlackBotClient(arguments)
        self.assertIsNotNone(client)

        self.assertEquals("SLACK_BOT_TOKEN", client._bot_token)

        self.assertEquals("Slack", client.bot.brain.properties.property("env"))

        self.assertIsInstance(client.get_client_configuration(), SlackConfiguration)

        self.assertIsInstance(client._slack_client, SlackClient)
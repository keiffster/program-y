import unittest.mock

from slack import WebClient

from programy.clients.polling.slack.client import SlackBotClient
from programy.clients.polling.slack.config import SlackConfiguration
from programy.clients.render.text import TextRenderer
from programytest.clients.arguments import MockArgumentParser


class MockSlackClient(object):

    def __init__(self, token, should_connect=True):
        self._token = token
        self._should_connect = should_connect

    def rtm_connect(self, with_team_state=True, **kwargs):
        return self._should_connect


class MockSlackBotClient(SlackBotClient):

    def __init__(self, argument_parser=None, slack_client=None, id="slackid"):
        self.test_slack_client = slack_client
        self.test_question = None
        self._id = id
        self._connect = True
        self.response_sent = None
        self.channel_sent = None
        SlackBotClient.__init__(self, argument_parser)

    def set_question(self, question):
        self.test_question = question

    def get_license_keys(self,):
         self._bot_token = "SLACK_BOT_TOKEN"

    def create_client(self):
        return MockSlackClient(self._bot_token)

    def connect(self):
        return self._connect

    def ask_question(self, sessionid, question):
        if self.test_question is not None:
            return self.test_question
        return super(MockSlackBotClient, self).ask_question(sessionid, question)

    def create_client(self):
        if self.test_slack_client is not None:
            return self.test_slack_client
        return super(MockSlackBotClient,self).create_client()

    def get_bot_id(self):
        return self._id

    def send_response(self, response, channel):
        self.response_sent = response
        self.channel_sent = channel


class SlackBotClientTests(unittest.TestCase):

    def test_slack_client_init(self):
        arguments = MockArgumentParser()
        client = MockSlackBotClient(arguments)
        self.assertIsNotNone(client)
        self.assertEqual("SLACK_BOT_TOKEN", client._bot_token)
        self.assertEqual('ProgramY AIML2.0 Client', client.get_description())
        self.assertIsInstance(client.get_client_configuration(), SlackConfiguration)
        self.assertIsInstance(client._slack_client, WebClient)

        self.assertFalse(client._render_callback())
        self.assertIsInstance(client.renderer, TextRenderer)

    def test_parse_direct_message(self):
        arguments = MockArgumentParser()
        client = MockSlackBotClient(arguments)

        text = "<@U024BE7LH> Hello"

        userid, message = client.parse_direct_message(text)
        self.assertIsNotNone(userid)
        self.assertEqual("U024BE7LH", userid)
        self.assertIsNotNone(message)
        self.assertEqual("Hello", message)

    def test_parse_mention(self):
        arguments = MockArgumentParser()
        client = MockSlackBotClient(arguments)

        text = "I told <@U024BE7LH> Hello"

        userid, message = client.parse_mention(text)
        self.assertIsNotNone(userid)
        self.assertEqual("U024BE7LH", userid)
        self.assertIsNotNone(message)
        self.assertEqual("Hello", message)

    def test_handle_message(self):
        arguments = MockArgumentParser()
        client = MockSlackBotClient(arguments)
        client._starterbot_id = "U024BE7LH"
        client.test_question = "Hi there"

        client.handle_message("Hello", "test", "U024BE7LH")

        self.assertIsNotNone(client.response_sent)
        self.assertEqual("Hi there", client.response_sent)
        self.assertIsNotNone(client.channel_sent)
        self.assertEqual("test", client.channel_sent)

    def test_parse_message(self):
        arguments = MockArgumentParser()
        client = MockSlackBotClient(arguments)
        client._starterbot_id = "U024BE7LH"
        client.test_question = "Hi there"

        event = {}
        event["text"] = "<@U024BE7LH> Hello"
        event["channel"] = "test"

        client.parse_message(event)

        self.assertIsNotNone(client.response_sent)
        self.assertEqual("Hi there", client.response_sent)
        self.assertIsNotNone(client.channel_sent)
        self.assertEqual("test", client.channel_sent)

    def test_parse_messages(self):
        arguments = MockArgumentParser()
        client = MockSlackBotClient(arguments)
        client._starterbot_id = "U024BE7LH"
        client.test_question = "Hi there"

        events = []
        events.append({"type": "message", "text": "<@U024BE7LH> Hello", "channel": "test"})

        client.parse_messages(events)

        self.assertIsNotNone(client.response_sent)
        self.assertEqual("Hi there", client.response_sent)
        self.assertIsNotNone(client.channel_sent)
        self.assertEqual("test", client.channel_sent)

    def poll_and_answer(self):
        arguments = MockArgumentParser()
        client = MockSlackBotClient(arguments)

        client.poll_and_answer()


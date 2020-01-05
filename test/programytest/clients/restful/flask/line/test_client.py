import unittest.mock

from linebot import LineBotApi, WebhookParser
from linebot.models import TextSendMessage
from linebot.webhook import SignatureValidator

from programy.clients.restful.flask.line.client import LineBotClient
from programy.clients.restful.flask.line.config import LineConfiguration
from programy.clients.render.text import TextRenderer
from programytest.clients.arguments import MockArgumentParser


class MockLineApi(LineBotApi):

    def __init__(self, channel_access_token):
        LineBotApi.__init__(self, channel_access_token)
        self._messages = []

    def reply_message(self, reply_token, messages, timeout=None):
        self._messages = messages


class MockSignatureValidator(SignatureValidator):

    def __init__(self, valid=True):
        self._valid = valid

    def validate(self, body, signature):
        return self._valid


class MockWebhookParser(WebhookParser):

    def __init__(self, channel_secret):
        self.signature_validator = MockSignatureValidator(channel_secret)


class MockLineBotClient(LineBotClient):

    def __init__(self, argument_parser=None, line_bot=None, parser=None):
        self._line_bot_api = line_bot
        self._parser = parser
        self.test_question = None
        LineBotClient.__init__(self, argument_parser)

    def set_question(self, question):
        self.test_question = question

    def get_license_keys(self):
        self._channel_secret = "LINE_CHANNEL_SECRET"
        self._channel_access_token = "LINE_ACCESS_TOKEN"

    def ask_question(self, sessionid, question):
        if self.test_question is not None:
            return self.test_question
        return super(MockLineBotClient, self).ask_question(sessionid, question)

    def create_line_bot(self):
        if self._line_bot_api is None:
            self._line_bot_api = LineBotApi(self._channel_access_token)
        if self._parser is None:
            self._parser = WebhookParser(self._channel_secret)

class LineBotClientTests(unittest.TestCase):

    def test_line_client_init(self):
        arguments = MockArgumentParser()
        client = MockLineBotClient(arguments)
        self.assertIsNotNone(client)

        self.assertEqual("LINE_CHANNEL_SECRET", client._channel_secret)
        self.assertEqual("LINE_ACCESS_TOKEN", client._channel_access_token)

        self.assertIsInstance(client.get_client_configuration(), LineConfiguration)
        self.assertEqual('ProgramY AIML2.0 Client', client.get_description())

        self.assertFalse(client._render_callback())
        self.assertIsInstance(client.renderer, TextRenderer)

    def test_handle_text_message(self):
        arguments = MockArgumentParser()
        client = MockLineBotClient(arguments, line_bot=MockLineApi("TOKEN"))
        self.assertIsNotNone(client)

        event = unittest.mock.Mock()
        event.message.unittest.mock.Mock()
        event.message.text = "Hello"
        event.source = unittest.mock.Mock()
        event.source.user_id = "User123"

        client.test_question = "Hi there"

        client.handle_text_message(event)

        self.assertIsNotNone(client._line_bot_api)
        self.assertIsNotNone(client._line_bot_api._messages)
        self.assertIsInstance(client._line_bot_api._messages, TextSendMessage)
        self.assertEqual("Hi there", client._line_bot_api._messages.text)

    def test_handle_unknown_message(self):
        arguments = MockArgumentParser()
        client = MockLineBotClient(arguments, line_bot=MockLineApi("TOKEN"))
        self.assertIsNotNone(client)

        event = unittest.mock.Mock()
        event.message.unittest.mock.Mock()
        event.message.text = "Hello"
        event.source = unittest.mock.Mock()
        event.source.user_id = "User123"

        client.test_question = "Unknown command"

        client.handle_unknown_message(event)

        self.assertIsNotNone(client._line_bot_api)
        self.assertIsNotNone(client._line_bot_api._messages)
        self.assertIsInstance(client._line_bot_api._messages, TextSendMessage)
        self.assertEqual("Unknown command", client._line_bot_api._messages.text)

    def test_handle_unknown_event(self):
        arguments = MockArgumentParser()
        client = MockLineBotClient(arguments, line_bot=MockLineApi("TOKEN"))
        self.assertIsNotNone(client)

        event = unittest.mock.Mock()
        event.message.unittest.mock.Mock()
        event.message.text = "Hello"
        event.source = unittest.mock.Mock()
        event.source.user_id = "User123"

        client.test_question = "Unknown command"

        client.handle_unknown_message(event)

        self.assertIsNotNone(client._line_bot_api)
        self.assertIsNotNone(client._line_bot_api._messages)
        self.assertIsInstance(client._line_bot_api._messages, TextSendMessage)
        self.assertEqual("Unknown command", client._line_bot_api._messages.text)

    def test_handle_message_request(self):
        arguments = MockArgumentParser()
        client = MockLineBotClient(arguments, line_bot=MockLineApi("TOKEN"), parser=MockWebhookParser("SECRET"))
        self.assertIsNotNone(client)

        body = '{"events": [{"type": "message", "source": {"source_id": "test", "type": "text", "user": {"user_id": "User123"}}}]}'
        signature = "SIGNATURE"

        client.handle_message_request(body, signature)

        self.assertIsNotNone(client._line_bot_api)
        self.assertIsNotNone(client._line_bot_api._messages)
        self.assertIsInstance(client._line_bot_api._messages, TextSendMessage)
        self.assertEqual("Unknown command", client._line_bot_api._messages.text)

    def test_receive_message(self):
        arguments = MockArgumentParser()
        client = MockLineBotClient(arguments, line_bot=MockLineApi("TOKEN"), parser=MockWebhookParser("SECRET"))
        self.assertIsNotNone(client)

        client.test_question = "Hi there"

        request = unittest.mock.Mock()
        request.headers = {'X-Line-Signature': "SECRET"}
        request.get_data.return_value = '{"events": [{"type": "message", "source": {"source_id": "test", "type": "text", "user": {"user_id": "User123"}}}]}'

        client.receive_message(request)

        self.assertIsNotNone(client._line_bot_api)
        self.assertIsNotNone(client._line_bot_api._messages)
        self.assertIsInstance(client._line_bot_api._messages, TextSendMessage)
        self.assertEqual("Unknown command", client._line_bot_api._messages.text)

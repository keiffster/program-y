import unittest.mock

from kik import KikApi
from kik.messages import TextMessage

from programy.clients.restful.flask.kik.client import KikBotClient
from programy.clients.restful.flask.kik.config import KikConfiguration
from programy.clients.render.text import TextRenderer
from programytest.clients.arguments import MockArgumentParser


class MockKikApi(KikApi):

    def __init__(self, bot, api_key):
        self._messages = []

    def send_messages(self, messages):
        self._messages = messages

    def verify_signature(self, signature, body):
        if signature is not None:
            return True
        return False


class MockHeaders():

    def __init__(self, signature=None):
        self._signature = signature

    def get(self, name):
        if name == 'X-Kik-Signature':
            return self._signature
        else:
            return None


class MockKikBotClient(KikBotClient):

    def __init__(self, argument_parser=None, kik_bot=None):
        self.test_question = None
        self._kik_bot = kik_bot
        KikBotClient.__init__(self, argument_parser)

    def set_question(self, question):
        self.test_question = question

    def get_license_keys(self):
        self._bot_api_key = "KIK_BOT_API_KEY"

    def ask_question(self, sessionid, question):
        if self.test_question is not None:
            return self.test_question
        return super(MockKikBotClient, self).ask_question(sessionid, question)

    def create_kik_bot(self):
        if self._kik_bot is not None:
            return self._kik_bot
        return super(MockKikBotClient,self).create_kik_bot()


class KikBotClientTests(unittest.TestCase):

    def test_kik_client_init(self):
        arguments = MockArgumentParser()
        client = MockKikBotClient(arguments, kik_bot=MockKikApi(bot="test", api_key="KEY"))
        self.assertIsNotNone(client)

        self.assertEqual("KIK_BOT_API_KEY", client._bot_api_key)

        self.assertIsInstance(client.get_client_configuration(), KikConfiguration)
        self.assertEqual('ProgramY AIML2.0 Client', client.get_description())

        self.assertIsInstance(client._kik_bot, KikApi)

        self.assertFalse(client._render_callback())
        self.assertIsInstance(client.renderer, TextRenderer)

    def test_handle_text_message(self):
        arguments = MockArgumentParser()
        client = MockKikBotClient(arguments, kik_bot=MockKikApi(bot="test", api_key="KEY"))
        self.assertIsNotNone(client)

        message = unittest.mock.Mock()
        message.body = "Hello"
        message.from_user = "User123"

        client.test_question = "Hi there"

        client.handle_text_message(message)

        self.assertIsNotNone(client._kik_bot)
        self.assertIsNotNone(client._kik_bot._messages)
        self.assertEqual(1, len(client._kik_bot._messages))
        self.assertIsInstance(client._kik_bot._messages[0], TextMessage)
        self.assertEqual("Hi there", client._kik_bot._messages[0].body)

    def test_handle_unknown_message(self):
        arguments = MockArgumentParser()
        client = MockKikBotClient(arguments, kik_bot=MockKikApi(bot="test", api_key="KEY"))
        self.assertIsNotNone(client)

        message = unittest.mock.Mock()
        message.body = "Hello"
        message.from_user = "User123"

        client.configuration.client_configuration._unknown_command_srai = "YKIK_UNKNOWN"
        client.test_question = "Unknown command"

        client.handle_unknown_message(message)

        self.assertIsNotNone(client._kik_bot)
        self.assertIsNotNone(client._kik_bot._messages)
        self.assertEqual(1, len(client._kik_bot._messages))
        self.assertIsInstance(client._kik_bot._messages[0], TextMessage)
        self.assertEqual("Unknown command", client._kik_bot._messages[0].body)

    def test_handle_message_request(self):
        arguments = MockArgumentParser()
        client = MockKikBotClient(arguments, kik_bot=MockKikApi(bot="test", api_key="KEY"))
        self.assertIsNotNone(client)

        request = unittest.mock.Mock()
        request.json = {"messages": [{"body": "Hello", "type": "text"}]}

        client.test_question = "Hi there"

        client.handle_message_request(request)

        self.assertIsNotNone(client._kik_bot)
        self.assertIsNotNone(client._kik_bot._messages)
        self.assertEqual(1, len(client._kik_bot._messages))
        self.assertIsInstance(client._kik_bot._messages[0], TextMessage)
        self.assertEqual("Hi there", client._kik_bot._messages[0].body)

    def test_handle_message_request_unknown(self):
        arguments = MockArgumentParser()
        client = MockKikBotClient(arguments, kik_bot=MockKikApi(bot="test", api_key="KEY"))
        self.assertIsNotNone(client)

        request = unittest.mock.Mock()
        request.json = {"messages": [{"body": "Hello", "type": "unknown"}]}

        client.configuration.client_configuration._unknown_command_srai = "YKIK_UNKNOWN"
        client.test_question = "Unknown command"

        client.handle_message_request(request)

        self.assertIsNotNone(client._kik_bot)
        self.assertIsNotNone(client._kik_bot._messages)
        self.assertEqual(1, len(client._kik_bot._messages))
        self.assertIsInstance(client._kik_bot._messages[0], TextMessage)
        self.assertEqual("Unknown command", client._kik_bot._messages[0].body)

    def test_receive_message_valid_message(self):
        arguments = MockArgumentParser()
        client = MockKikBotClient(arguments, kik_bot=MockKikApi(bot="test", api_key="KEY"))
        self.assertIsNotNone(client)

        request = unittest.mock.Mock()
        request.headers = MockHeaders("LKHLKJGKJHGKJHGKJHGHJK")
        request.json = {"messages": [{"body": "Hello", "type": "text"}]}

        response = client.receive_message(request)
        self.assertIsNotNone(response)
        self.assertEqual("200 OK", response.status)

    def test_receive_message_invalid_message(self):
        arguments = MockArgumentParser()
        client = MockKikBotClient(arguments, kik_bot=MockKikApi(bot="test", api_key="KEY"))
        self.assertIsNotNone(client)

        request = unittest.mock.Mock()
        request.headers = MockHeaders()
        request.json = {"messages": [{"body": "Hello", "type": "text"}]}

        response = client.receive_message(request)
        self.assertIsNotNone(response)
        self.assertEqual("403 FORBIDDEN", response.status)

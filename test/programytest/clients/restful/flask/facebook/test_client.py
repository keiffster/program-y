import unittest.mock

from pymessenger.bot import Bot

from programy.clients.restful.flask.facebook.client import FacebookBotClient
from programy.clients.restful.flask.facebook.config import FacebookConfiguration
from programy.clients.restful.flask.facebook.renderer import FacebookRenderer
from programytest.clients.arguments import MockArgumentParser


class MockFacebookBot(Bot):

    def __init__(self, access_token):
        self._access_token = access_token
        self._recipient_id = None
        self._message = None
        self.payload = None

    def render_response(self, recipient_id, message):
        self._recipient_id = recipient_id
        self._message = message

    def send_raw(self, payload):
        self.payload = payload


class MockFacebookBotClient(FacebookBotClient):

    def __init__(self, argument_parser=None):
        self._access_token = None
        self._verify_token = None
        FacebookBotClient.__init__(self, argument_parser)
        self.test_question = None

    def set_question(self, question):
        self.test_question = question

    def get_license_keys(self):
        self._access_token = "FACEBOOK_ACCESS_TOKEN"
        self._verify_token = "FACEBOOK_VERIFY_TOKEN"

    def ask_question(self, sessionid, question):
        if self.test_question is not None:
            return self.test_question
        return super(MockFacebookBotClient, self).ask_question(sessionid, question)

    def create_facebook_bot(self):
        return MockFacebookBot(self._access_token)


class FacebookClientBotClientTests(unittest.TestCase):

    def test_facebook_client_init(self):
        arguments = MockArgumentParser()
        client = MockFacebookBotClient(arguments)
        self.assertIsNotNone(client)

        self.assertEqual("FACEBOOK_VERIFY_TOKEN", client._verify_token)
        self.assertEqual("FACEBOOK_ACCESS_TOKEN", client._access_token)

        self.assertIsInstance(client.get_client_configuration(), FacebookConfiguration)
        self.assertEqual('ProgramY AIML2.0 Client', client.get_description())

        self.assertIsInstance(client._facebook_bot, Bot)

        self.assertTrue(client._render_callback())
        self.assertIsInstance(client.renderer, FacebookRenderer)

    def test_hub_challenge(self):
        arguments = MockArgumentParser()
        client = MockFacebookBotClient(arguments)

        request = unittest.mock.Mock()
        request.args =unittest.mock.Mock()
        request.args.get.return_value = "XXZZ"
        self.assertEqual("XXZZ", client.get_hub_challenge(request))

    def test_hub_verify_token(self):
        arguments = MockArgumentParser()
        client = MockFacebookBotClient(arguments)

        request = unittest.mock.Mock()
        request.args =unittest.mock.Mock()
        request.args.get.return_value = "XXZZ"
        self.assertEqual("XXZZ", client.get_hub_verify_token(request))

    def test_verify_fb_token(self):
        arguments = MockArgumentParser()
        client = MockFacebookBotClient(arguments)

        request = unittest.mock.Mock()
        request.args =unittest.mock.Mock()
        request.args.get.return_value = "ZZZZZZ"

        client._verify_token = "XXXXXX"
        self.assertEqual("ZZZZZZ", client.verify_fb_token("XXXXXX", request))

    def test_render_response(self):
        arguments = MockArgumentParser()
        client = MockFacebookBotClient(arguments)

        client.render_response(client.create_client_context("user1"), "hello")

        self.assertIsNotNone(client._facebook_bot.payload)

    def test_return_hub_challenge(self):
        arguments = MockArgumentParser()
        client = MockFacebookBotClient(arguments)

        request = unittest.mock.Mock()
        request.args = unittest.mock.Mock()
        request.args.get.return_value = "ZZZZZZ"

        client._verify_token = "ZZZZZZ"

        self.assertEqual("ZZZZZZ", client.return_hub_challenge(request))

    def test_get_message_text(self):
        arguments = MockArgumentParser()
        client = MockFacebookBotClient(arguments)

        message = {}
        message['message'] = unittest.mock.Mock()
        message['message'].get.return_value = "Hello"

        self.assertEqual("Hello", client.get_message_text(message))

    def has_attachements(self):
        arguments = MockArgumentParser()
        client = MockFacebookBotClient(arguments)

        arguments = MockArgumentParser()
        client = MockFacebookBotClient(arguments)

        message = {}
        message['message'] = unittest.mock.Mock()
        message['message'].get.return_value = "Hello"

        self.assertEqual("Hello", client.get_message_text(message))

    def test_get_recipitent_id(self):
        arguments = MockArgumentParser()
        client = MockFacebookBotClient(arguments)

        message = {'message': {'sender': {'id': 'user1'}}}
        message['message'] = unittest.mock.Mock()
        message['message'].get.return_value = []

        self.assertTrue(client.has_attachements(message))

    def test_process_facebook_request(self):
        arguments = MockArgumentParser()
        client = MockFacebookBotClient(arguments)
        client.test_question = "Hi there"

        request = {'entry': [{'messaging': [{'message': {"text": "Hello"}, 'sender': {'id': 'user1'}}]}]}

        client.process_facebook_request(request)

        self.assertIsNotNone(client._facebook_bot.payload)

    def test_process_facebook_message(self):
        arguments = MockArgumentParser()
        client = MockFacebookBotClient(arguments)
        client.test_question = "Hi there"

        messaging = [{'message': {"text": "Hello"}, 'sender': {'id': 'user1'}}]

        client.process_facebook_message(messaging)

        self.assertIsNotNone(client._facebook_bot.payload)

    def test_handle_message(self):
        arguments = MockArgumentParser()
        client = MockFacebookBotClient(arguments)
        client.test_question = "Hi there"

        message = {'message': {"text": "Hello"}, 'sender': {'id': 'user1'}}

        client.handle_message(message)

        self.assertIsNotNone(client._facebook_bot.payload)

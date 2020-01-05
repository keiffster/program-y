import logging
import unittest.mock

from viberbot import Api
from viberbot.api.user_profile import UserProfile
from viberbot.api.viber_requests import ViberConversationStartedRequest
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest
from viberbot.api.viber_requests import ViberUnsubscribedRequest

from programy.clients.restful.flask.viber.client import ViberBotClient
from programy.clients.restful.flask.viber.config import ViberConfiguration
from programy.clients.render.text import TextRenderer
from programytest.clients.arguments import MockArgumentParser


class MockViberApi(Api):

    def __init__(self, configuration, request=None, verified=True):
        self._logger = logging.getLogger()
        self._messages = []
        self._request = request
        self._verified = verified

    def set_webhook(self, url, webhook_events=None, is_inline=False):
        pass

    def send_messages(self, to, messages, chat_id=None):
        self._messages = messages

    def verify_signature(self, request_data, signature):
	    return self._verified

    def parse_request(self, request_data):
        if self._request is None:
            super(MockViberApi, self).parse_request(request_data)
        return self._request


class MockViberBotClient(ViberBotClient):

    def __init__(self, argument_parser=None, viber_client=None):
        self.test_viber_client = viber_client
        self.test_question = None
        ViberBotClient.__init__(self, argument_parser)

    def parse_configuration(self):
        self.configuration.client_configuration._name = "ViberBot"
        self.configuration.client_configuration._avatar = "viber.svg"
        self.configuration.client_configuration._webhook = "http://localhost/webhook"

    def set_question(self, question):
        self.test_question = question

    def get_license_keys(self):
        self._viber_token = "VIBER_TOKEN"

    def ask_question(self, sessionid, question):
        if self.test_question is not None:
            return self.test_question
        return super(MockViberBotClient, self).ask_question(sessionid, question)

    def create_viber_api(self, configuration):
        return MockViberApi(configuration)

    def create_viber_bot(self, viber_token):
        if self.test_viber_client is not None:
            return self.test_viber_client
        return super(MockViberBotClient,self).create_viber_bot(viber_token)


class ViberBotClientTests(unittest.TestCase):

    def test_viber_client_init(self):
        arguments = MockArgumentParser()
        client = MockViberBotClient(arguments)
        self.assertIsNotNone(client)

        self.assertEqual("VIBER_TOKEN", client._viber_token)
        self.assertIsNotNone(client._viber_bot)

        self.assertIsInstance(client.get_client_configuration(), ViberConfiguration)

        self.assertIsInstance(client._viber_bot, Api)

        self.assertFalse(client._render_callback())
        self.assertIsInstance(client.renderer, TextRenderer)

    def test_create_viber_bot_no_token(self):
        arguments = MockArgumentParser()
        client = MockViberBotClient(arguments)
        self.assertIsNotNone(client)

        bot = client.create_viber_bot(None)
        self.assertIsNone(bot)

    def test_create_viber_bot_no_name(self):
        arguments = MockArgumentParser()
        client = MockViberBotClient(arguments)
        self.assertIsNotNone(client)

        client.configuration.client_configuration._name = None

        bot = client.create_viber_bot("TOKEN")
        self.assertIsNone(bot)

    def test_create_viber_bot_no_avatar(self):
        arguments = MockArgumentParser()
        client = MockViberBotClient(arguments)
        self.assertIsNotNone(client)

        client.configuration.client_configuration._avatar = None

        bot = client.create_viber_bot("TOKEN")
        self.assertIsNone(bot)

    def test_create_viber_bot_no_webhook(self):
        arguments = MockArgumentParser()
        client = MockViberBotClient(arguments)
        self.assertIsNotNone(client)

        client.configuration.client_configuration._webhook = None

        bot = client.create_viber_bot("TOKEN")
        self.assertIsNone(bot)

    def test_handle_message_request(self):
        arguments = MockArgumentParser()
        client = MockViberBotClient(arguments, viber_client=MockViberApi(None))
        self.assertIsNotNone(client)

        request = ViberMessageRequest()
        request._message = "Hello"
        request._sender = UserProfile(user_id="User123")

        client.test_question = "Hi there"

        client.handle_message_request(request)

        self.assertIsNotNone(client.test_viber_client)
        self.assertIsNotNone(client.test_viber_client._messages)
        self.assertEqual(1, len(client.test_viber_client._messages))
        self.assertEqual("Hi there", client.test_viber_client._messages[0].text)

    def test_handle_subscribed_request(self):
        arguments = MockArgumentParser()
        client = MockViberBotClient(arguments, viber_client=MockViberApi(None))
        self.assertIsNotNone(client)

        request = ViberSubscribedRequest ()
        request._user = UserProfile(user_id="User123")

        client.handle_subscribed_request(request)

        self.assertIsNotNone(client.test_viber_client)
        self.assertIsNotNone(client.test_viber_client._messages)
        self.assertEqual(1, len(client.test_viber_client._messages))
        self.assertEqual("Thanks for subscribing!", client.test_viber_client._messages[0].text)

    def test_handle_unsubscribed_request(self):
        arguments = MockArgumentParser()
        client = MockViberBotClient(arguments, viber_client=MockViberApi(None))
        self.assertIsNotNone(client)

        request = ViberUnsubscribedRequest()
        request._user_id = "User123"

        client.handle_unsubscribed_request(request)

    def test_handle_conversation_started_request(self):
        arguments = MockArgumentParser()
        client = MockViberBotClient(arguments, viber_client=MockViberApi(None))
        self.assertIsNotNone(client)

        request = ViberConversationStartedRequest()
        request._user = UserProfile(user_id="User123")

        client.handle_conversation_started_request(request)

    def test_handle_failed_request(self):
        arguments = MockArgumentParser()
        client = MockViberBotClient(arguments, viber_client=MockViberApi(None))
        self.assertIsNotNone(client)

        request = ViberFailedRequest()
        request._user_id = "User123"
        request._desc = "Whoops, I know nothing!"

        client.handle_failed_request(request)

    def test_handle_unknown_request(self):
        arguments = MockArgumentParser()
        client = MockViberBotClient(arguments, viber_client=MockViberApi(None))
        self.assertIsNotNone(client)

        request = unittest.mock.Mock()

        client.handle_unknown_request(request)

    def test_receive_message(self):
        arguments = MockArgumentParser()
        viber_api = MockViberApi(None)
        client = MockViberBotClient(arguments, viber_client=viber_api)
        self.assertIsNotNone(client)

        request = unittest.mock.Mock()
        request.get_data.return_value = "{}"
        request.headers = {"X-Viber-Content-Signature": "SIGNATURE"}

        return_request = ViberMessageRequest()
        return_request._message = "Hello"
        return_request._sender = UserProfile(user_id="User123")
        viber_api._request = return_request

        client.receive_message(request)
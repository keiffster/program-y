import unittest.mock
from pymessenger.bot import Bot

from programy.clients.restful.flask.facebook.client import FacebookBotClient, FacebookBot
from programy.clients.restful.flask.facebook.config import FacebookConfiguration

from programytest.clients.arguments import MockArgumentParser

class MockFacebookBot(FacebookBot):

    def __init__(self, access_token):
        pass

    def send_message(self, recipient_id, message):
        self._recipient_id = recipient_id
        self._message = message


class MockFacebookBotClient(FacebookBotClient):

    def __init__(self, argument_parser=None):
        self.test_question = None
        FacebookBotClient.__init__(self, argument_parser)

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


class FacebookBotClientTests(unittest.TestCase):

    def test_facebook_client_init(self):
        arguments = MockArgumentParser()
        client = MockFacebookBotClient(arguments)
        self.assertIsNotNone(client)

        self.assertEquals("FACEBOOK_VERIFY_TOKEN", client._verify_token)
        self.assertEquals("FACEBOOK_ACCESS_TOKEN", client._access_token)

        self.assertIsInstance(client.get_client_configuration(), FacebookConfiguration)
        self.assertEquals('ProgramY AIML2.0 Facebook Client', client.get_description())

        self.assertIsInstance(client._facebook_bot, FacebookBot)

    def test_hub_challenge(self):
        arguments = MockArgumentParser()
        client = MockFacebookBotClient(arguments)

        request = unittest.mock.Mock()
        request.args =unittest.mock.Mock()
        request.args.get.return_value = "XXZZ"
        self.assertEquals("XXZZ", client.get_hub_challenge(request))

    def test_hub_verify_token(self):
        arguments = MockArgumentParser()
        client = MockFacebookBotClient(arguments)

        request = unittest.mock.Mock()
        request.args =unittest.mock.Mock()
        request.args.get.return_value = "XXZZ"
        self.assertEquals("XXZZ", client.get_hub_verify_token(request))

    def test_verify_fb_token(self):
        arguments = MockArgumentParser()
        client = MockFacebookBotClient(arguments)

        request = unittest.mock.Mock()
        request.args =unittest.mock.Mock()
        request.args.get.return_value = "ZZZZZZ"

        client._verify_token = "XXXXXX"
        self.assertEquals("ZZZZZZ", client.verify_fb_token("XXXXXX", request))

    def test_send_message(self):
        arguments = MockArgumentParser()
        client = MockFacebookBotClient(arguments)

        client.send_message("user1", "hello")
        self.assertEquals("user1", client._facebook_bot._recipient_id)
        self.assertEquals("hello", client._facebook_bot._message)

    def test_return_hub_challenge(self):
        arguments = MockArgumentParser()
        client = MockFacebookBotClient(arguments)

        request = unittest.mock.Mock()
        request.args = unittest.mock.Mock()
        request.args.get.return_value = "ZZZZZZ"

        client._verify_token = "ZZZZZZ"

        self.assertEquals("ZZZZZZ", client.return_hub_challenge(request))

    def test_get_message_text(self):
        arguments = MockArgumentParser()
        client = MockFacebookBotClient(arguments)

        message = {}
        message['message'] = unittest.mock.Mock()
        message['message'].get.return_value = "Hello"

        self.assertEquals("Hello", client.get_message_text(message))

    def has_attachements(self):
        arguments = MockArgumentParser()
        client = MockFacebookBotClient(arguments)

        arguments = MockArgumentParser()
        client = MockFacebookBotClient(arguments)

        message = {}
        message['message'] = unittest.mock.Mock()
        message['message'].get.return_value = "Hello"

        self.assertEquals("Hello", client.get_message_text(message))

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

        message = unittest.mock.Mock()
        message.get.return_value = "hello"

        request = {'entry': [{'messaging': [{'message': message, 'sender': {'id': 'user1'}}]}]}

        client.process_facebook_request(request)

        self.assertEquals("user1", client._facebook_bot._recipient_id)
        self.assertEquals("Hi there", client._facebook_bot._message)

    def test_process_facebook_message(self):
        arguments = MockArgumentParser()
        client = MockFacebookBotClient(arguments)
        client.test_question = "Hi there"

        message = unittest.mock.Mock()
        message.get.return_value = "hello"

        messaging = [{'message': message, 'sender': {'id': 'user1'}}]

        client.process_facebook_message(messaging)

        self.assertEquals("user1", client._facebook_bot._recipient_id)
        self.assertEquals("Hi there", client._facebook_bot._message)

    def test_handle_message(self):
        arguments = MockArgumentParser()
        client = MockFacebookBotClient(arguments)
        client.test_question = "Hi there"

        inner_message = unittest.mock.Mock()
        inner_message.get.return_value = "hello"

        message = {'message': inner_message, 'sender': {'id': 'user1'}}

        client.handle_message(message)

        self.assertEquals("user1", client._facebook_bot._recipient_id)
        self.assertEquals("Hi there", client._facebook_bot._message)

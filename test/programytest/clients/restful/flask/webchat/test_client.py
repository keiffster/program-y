import unittest
import unittest.mock

from programy.clients.restful.flask.webchat.client import WebChatBotClient
from programy.clients.restful.flask.webchat.config import WebChatConfiguration

from programytest.clients.arguments import MockArgumentParser


class MockWebChatBotClient(WebChatBotClient):

    def __init__(self, argument_parser=None):
        self.test_answer = None
        WebChatBotClient.__init__(self, argument_parser)

    def unauthorised_access_response(self, error_code=401):
        return "Unauthorised Access"

    def get_default_response(self, client_context):
        return "Sorry"

    def create_response(self, response_data, userid, userid_expire_date):
        return {'response': response_data}

    def get_answer(self, client_context, question):
        if self.test_answer is not None:
            return self.test_answer
        return super(WebChatBotClient, self).get_answer(client_context, question)


class WebChatBotClientTests(unittest.TestCase):

    def test_webchat_client_init(self):
        arguments = MockArgumentParser()
        client = MockWebChatBotClient(arguments)
        self.assertIsNotNone(client)
        client.initialise()

        self.assertIsInstance(client.get_client_configuration(), WebChatConfiguration)
        self.assertEqual('ProgramY AIML2.0 Client', client.get_description())

    def test_api_keys(self):
        arguments = MockArgumentParser()
        client = MockWebChatBotClient(arguments)
        self.assertIsNotNone(client)
        client.initialise()

        client.api_keys.api_keys = ['KEY1', 'KEY2']

        self.assertTrue(client.api_keys.is_apikey_valid('KEY1'))
        self.assertTrue(client.api_keys.is_apikey_valid('KEY2'))
        self.assertFalse(client.api_keys.is_apikey_valid('KEY3'))

    def test_get_api_key_exists(self):
        arguments = MockArgumentParser()
        client = MockWebChatBotClient(arguments)
        self.assertIsNotNone(client)
        client.initialise()

        client.api_keys.api_keys = ['KEY1', 'KEY2']

        request = unittest.mock.Mock
        request.args = {'apikey': 'KEY1'}

        key = client.api_keys.get_api_key(request)
        self.assertIsNotNone(key)
        self.assertEqual('KEY1', key)

    def test_get_api_key_not_exists(self):
        arguments = MockArgumentParser()
        client = MockWebChatBotClient(arguments)
        self.assertIsNotNone(client)
        client.initialise()

        request = unittest.mock.Mock
        request.args = {}

        key = client.api_keys.get_api_key(request)
        self.assertIsNone(key)

    def test_get_question_exists(self):
        arguments = MockArgumentParser()
        client = MockWebChatBotClient(arguments)
        self.assertIsNotNone(client)

        request = unittest.mock.Mock
        request.args = {'question': 'Hello'}

        key = client.get_question(request)
        self.assertIsNotNone(key)
        self.assertEqual('Hello', key)

    def test_get_question_not_exists(self):
        arguments = MockArgumentParser()
        client = MockWebChatBotClient(arguments)
        self.assertIsNotNone(client)

        request = unittest.mock.Mock
        request.args = {}

        key = client.get_question(request)
        self.assertIsNone(key)

    def test_check_api_key_not_required(self):
        arguments = MockArgumentParser()
        client = MockWebChatBotClient(arguments)
        self.assertIsNotNone(client)

        request = unittest.mock.Mock
        request.args = {}

        client.configuration.client_configuration._use_api_keys = False
        self.assertTrue(client.api_keys.verify_api_key_usage(request))

    def test_check_api_key_required_valid(self):
        arguments = MockArgumentParser()
        client = MockWebChatBotClient(arguments)
        self.assertIsNotNone(client)

        request = unittest.mock.Mock
        request.args = {'apikey': "KEY1"}

        client.configuration.client_configuration._use_api_keys = True
        client.api_keys.api_keys = ['KEY1']

        self.assertTrue(client.api_keys.verify_api_key_usage(request))

    def test_check_api_key_required_key_missing(self):
        arguments = MockArgumentParser()
        client = MockWebChatBotClient(arguments)
        self.assertIsNotNone(client)

        request = unittest.mock.Mock
        request.args = {}

        client.configuration.client_configuration._use_api_keys = True
        client.api_keys.api_keys = ['KEY1']

        self.assertFalse(client.api_keys.verify_api_key_usage(request))

    def test_check_api_key_required_key_invalid(self):
        arguments = MockArgumentParser()
        client = MockWebChatBotClient(arguments)
        self.assertIsNotNone(client)
        client.initialise()

        request = unittest.mock.Mock
        request.args = {'KEY2'}

        client.configuration.client_configuration._use_api_keys = True
        client.api_keys.api_keys = ['KEY1']

        self.assertFalse(client.api_keys.verify_api_key_usage(request))

    def test_get_userid_present(self):
        arguments = MockArgumentParser()
        client = MockWebChatBotClient(arguments)
        self.assertIsNotNone(client)
        client.initialise()

        request = unittest.mock.Mock()
        request.cookies = unittest.mock.Mock()
        request.cookies.get.return_value = "User123"

        self.assertEqual("User123", client.get_userid(request))

    def test_get_userid_missing(self):
        arguments = MockArgumentParser()
        client = MockWebChatBotClient(arguments)
        self.assertIsNotNone(client)
        client.initialise()

        request = unittest.mock.Mock()
        request.cookies = unittest.mock.Mock()
        request.cookies.get.return_value = None

        self.assertIsNotNone(client.get_userid(request))

    def test_create_success_response_data(self):
        arguments = MockArgumentParser()
        client = MockWebChatBotClient(arguments)
        self.assertIsNotNone(client)
        client.initialise()

        response = client.create_success_response_data("Hello", "Hi there")
        self.assertIsNotNone(response)
        self.assertEqual({"question": "Hello", "answer": "Hi there"}, response)

    def test_create_error_response_data(self):
        arguments = MockArgumentParser()
        client = MockWebChatBotClient(arguments)
        self.assertIsNotNone(client)

        client_context = client.create_client_context("User123")

        response = client.create_error_response_data(client_context, "Hello", "Whoops!")
        self.assertIsNotNone(response)
        self.assertEqual({"question": "Hello", "answer": "Sorry", "error": "Whoops!"}, response)

    def test_get_userid_cookie_expirary_date(self):
        arguments = MockArgumentParser()
        client = MockWebChatBotClient(arguments)
        self.assertIsNotNone(client)

        expirary = client.get_userid_cookie_expirary_date(10)
        self.assertIsNotNone(expirary)

    def test_receive_message(self):
        arguments = MockArgumentParser()
        client = MockWebChatBotClient(arguments)
        self.assertIsNotNone(client)

        client.configuration.client_configuration._use_api_keys = False

        client.test_answer = "Hi there"

        request = unittest.mock.Mock()
        request.args = {"question": "Hello"}
        request.cookies = unittest.mock.Mock()
        request.cookies.get.return_value = "User123"

        response = client.receive_message(request)
        self.assertIsNotNone(response)
        self.assertEqual({'response': {'answer': 'Hi there', 'question': 'Hello'}}, response)
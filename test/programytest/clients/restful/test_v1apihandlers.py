import unittest

from programy.clients.restful.apihandlers import APIHandler_V1_0

class MockBot(object):

    def __init__(self):
        self.default_response = "default response"


class MockClientContext(object):

    def __init__(self, bot):
        self.bot = bot


class MockBotClient(object):

    def __init__(self, verify_api_key_usage=(None, None), variables={}, response=None):
        self._verify_api_key_usage = verify_api_key_usage
        self._variables = variables
        self._response = response

    def verify_api_key_usage(self, request, method='GET'):
        return self._verify_api_key_usage[0],  self._verify_api_key_usage[1]

    def get_variable(self, request, name, method):
        return self._variables[name]

    def ask_question(self, userid, question, metadata=None):
        return self._response

    def create_client_context(self, userid):
        return MockClientContext(MockBot())


class APIHandler_V1_0Tests(unittest.TestCase):

    def test_init(self):
        mock_bot_client = MockBotClient()
        self.assertIsNotNone(mock_bot_client)

        handler = APIHandler_V1_0(mock_bot_client)
        self.assertIsNotNone(handler)

    def test_process_get_request(self):
        mock_bot_client = MockBotClient(variables={"question": "question", "userid": "userid"}, response="Hello")
        self.assertIsNotNone(mock_bot_client)

        handler = APIHandler_V1_0(mock_bot_client)
        self.assertIsNotNone(handler)

        response = handler.process_request("Hello")
        self.assertIsNotNone(response)
        self.assertEquals(response, ({'response': {'question': 'question', 'answer': "Hello", 'userid': 'userid'}}, 200))

    def test_format_success_response(self):
        mock_bot_client = MockBotClient()
        self.assertIsNotNone(mock_bot_client)

        handler = APIHandler_V1_0(mock_bot_client)
        self.assertIsNotNone(handler)

        response = handler.format_success_response("userid1", "Hello", "Hi there")
        self.assertIsNotNone(response)
        self.assertEquals(response, {'response': {"question": "Hello", "answer": "Hi there", "userid": "userid1"}})

    def test_format_error_response(self):
        mock_bot_client = MockBotClient()
        self.assertIsNotNone(mock_bot_client)

        handler = APIHandler_V1_0(mock_bot_client)
        self.assertIsNotNone(handler)

        response = handler.format_error_response("userid1", "Hello", "Oopsie")
        self.assertIsNotNone(response)
        self.assertEquals(response, {'response': {"question": "Hello", "answer": "default response", "userid": "userid1", "error": "Oopsie"}})

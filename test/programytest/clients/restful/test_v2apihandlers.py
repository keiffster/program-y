import unittest

from programy.clients.restful.apihandlers import APIHandler_V2_0

class MockBot(object):

    def __init__(self):
        self.default_response = "default response"


class MockClientContext(object):

    def __init__(self, bot):
        self.bot = bot


class MockBotClient(object):

    def __init__(self, verify_api_key_usage=(None, None), variables={}, response=None, metadata={}):
        self._verify_api_key_usage = verify_api_key_usage
        self._variables = variables
        self._response = response
        self._metadata = metadata

    def verify_api_key_usage(self, request, method='GET'):
        return self._verify_api_key_usage[0],  self._verify_api_key_usage[1]

    def get_variable(self, request, name, method):
        return self._variables[name]

    def ask_question(self, userid, question, metadata=None):
        metadata["botName"] = self._metadata["botName"]
        metadata["version"] = self._metadata["version"]
        metadata["copyright"] = self._metadata["copyright"]
        metadata["authors"] = self._metadata["authors"]
        return self._response

    def create_client_context(self, userid):
        return MockClientContext(MockBot())


class APIHandler_V2_0UnderTest(APIHandler_V2_0):

    def __init__(self, bot_client):
        APIHandler_V2_0.__init__(self, bot_client)

    def _get_timestamp(self):
        return 0


class APIHandler_V2_0Tests(unittest.TestCase):

    def test_init(self):
        mock_bot_client = MockBotClient()
        self.assertIsNotNone(mock_bot_client)

        handler = APIHandler_V2_0(mock_bot_client)
        self.assertIsNotNone(handler)

    def test_process_get_request(self):
        mock_bot_client = MockBotClient(variables={"query": "Hello",
                                                   "userId": "userid1"
                                                  },
                                        response="Hi there",
                                        metadata={ "botName": "testbot",
                                                   "version": "1.0",
                                                   "copyright": "copyright 2019'",
                                                   "authors": "Test Bot"
                                                  })
        self.assertIsNotNone(mock_bot_client)

        handler = APIHandler_V2_0UnderTest(mock_bot_client)
        self.assertIsNotNone(handler)

        response = handler.process_request("Hello")
        self.assertIsNotNone(response)
        self.assertEquals(response, ({'response': {"query": "Hello",
                                                   "userId": "userid1",
                                                   "timestamp": 0,
                                                   "text": "Hi there",
                                     },
                                    'status': {
                                        'code': 200,
                                        'message': 'success'
                                    },
                                    "meta": {
                                        "botName": "testbot",
                                        "version": "1.0",
                                        "copyright": "copyright 2019'",
                                        "authors": "Test Bot"
                                    }
                                    }, 200))

    def test_format_success_response(self):
        mock_bot_client = MockBotClient(variables={"query": "Hello",
                                                   "userId": "userid1"
                                                  },
                                        response="Hi there",
                                        )
        self.assertIsNotNone(mock_bot_client)

        handler = APIHandler_V2_0UnderTest(mock_bot_client)
        self.assertIsNotNone(handler)

        metadata = {"botName": "testbot",
                    "version": "1.0",
                    "copyright": "copyright 2019'",
                    "authors": "Test Bot"
                    }
        response = handler.format_success_response("userid1", "Hello", "Hi there", metadata)
        self.assertIsNotNone(response)
        self.assertEquals(response, {'response': {"query": "Hello",
                                                   "userId": "userid1",
                                                   "timestamp": 0,
                                                   "text": "Hi there",
                                     },
                                    'status': {
                                        'code': 200,
                                        'message': 'success'
                                    },
                                    "meta": {
                                        "botName": "testbot",
                                        "version": "1.0",
                                        "copyright": "copyright 2019'",
                                        "authors": "Test Bot"
                                    }})

    def test_format_error_response(self):
        mock_bot_client = MockBotClient()
        self.assertIsNotNone(mock_bot_client)

        handler = APIHandler_V2_0UnderTest(mock_bot_client)
        self.assertIsNotNone(handler)

        metadata = {"botName": "testbot",
                    "version": "1.0",
                    "copyright": "copyright 2019'",
                    "authors": "Test Bot"
                    }
        response = handler.format_error_response("userid1", "Hello", "Oopsie", metadata)
        self.assertIsNotNone(response)
        self.assertEquals(response, {'response': {"query": "Hello",
                                                   "userId": "userid1",
                                                   "timestamp": 0,
                                     },
                                    'status': {
                                        'code': 500,
                                        'message': 'Oopsie'
                                    },
                                    "meta": {
                                        "botName": "testbot",
                                        "version": "1.0",
                                        "copyright": "copyright 2019'",
                                        "authors": "Test Bot"
                                    }})

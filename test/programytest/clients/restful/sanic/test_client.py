import unittest
import unittest.mock
import os

from programytest.clients.arguments import MockArgumentParser

if os.name != "nt":
    from programy.clients.restful.sanic.client import SanicRestBotClient

    class MockSanicRestBotClient(SanicRestBotClient):

        def __init__(self, argument_parser=None):
            SanicRestBotClient.__init__(self, "sanic", argument_parser)
            self.aborted = False
            self.answer = None
            self.ask_question_exception = False

        def server_abort(self, message, status_code):
            self.aborted = True
            raise Exception("Pretending to abort!")

        def ask_question(self, userid, question):
            if self.ask_question_exception is True:
                raise Exception("Something bad happened")
            return self.answer


    class SanicRestBotClientTests(unittest.TestCase):
    
        def test_rest_client_init(self):
            arguments = MockArgumentParser()
            client = SanicRestBotClient("flask", arguments)
            self.assertIsNotNone(client)
    
        def test_verify_api_key_usage_inactive(self):
            arguments = MockArgumentParser()
            client = SanicRestBotClient("flask", arguments)
            self.assertIsNotNone(client)
            client.configuration.client_configuration._use_api_keys = False
            request = unittest.mock.Mock()
            self.assertTrue(client.api_keys.verify_api_key_usage(request))
    
        def test_get_api_key(self):
            arguments = MockArgumentParser()
            client = SanicRestBotClient("flask", arguments)
    
            request = unittest.mock.Mock()
            request.args = {}
            request.args['apikey'] = '11111111'
    
            self.assertEqual('11111111', client.api_keys.get_api_key(request))
    
        def test_verify_api_key_usage_active(self):
            arguments = MockArgumentParser()
            client = SanicRestBotClient("flask", arguments)
            self.assertIsNotNone(client)
            client.configuration.client_configuration._use_api_keys = True
            client.configuration.client_configuration._api_key_file = os.path.dirname(__file__) + os.sep + ".." + os.sep + ".." + os.sep + "api_keys.txt"
            client.initialise()
            request = unittest.mock.Mock()
            request.args = {}
            request.args['apikey'] = '11111111'
            self.assertTrue(client.api_keys.verify_api_key_usage(request))
    
        def test_verify_api_key_usage_active_no_apikey(self):
            arguments = MockArgumentParser()
            client = MockSanicRestBotClient(arguments)
            client.configuration.client_configuration._use_api_keys = True
            client.initialise()

            request = unittest.mock.Mock()
            request.args = {}
    
            self.assertFalse(client.api_keys.verify_api_key_usage(request))

        def test_verify_api_key_usage_active_invalid_apikey(self):
            arguments = MockArgumentParser()
            client = MockSanicRestBotClient(arguments)
            client.configuration.client_configuration._use_api_keys = True
    
            request = unittest.mock.Mock()
            request.args = {}
            request.args['apikey'] = 'invalid'
    
            self.assertFalse(client.api_keys.verify_api_key_usage(request))


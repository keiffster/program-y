import unittest
import os
import json

from programy.utils.license.keys import LicenseKeys
from programy.utils.services.pannous import PannousService, PannousAPI
from programy.utils.services.service import BrainServiceConfiguration
from test.utils.services.mock_requests import MockRequestsAPI

class PannousAPITests(unittest.TestCase):

    def test_ask_question_valid_json(self):

        request_api = MockRequestsAPI()
        pannous_api = PannousAPI(request_api=request_api)
        request_api._response = json.loads("""
        {
            "output": [
                { "actions": { "say": {"text": "Hello"} } }
            ]
        }
        """)
        response = pannous_api.ask_question("http://testurl", "Hello", "testid")
        self.assertEquals(response, "Hello")

    def test_ask_question_no_response(self):

        with self.assertRaises(Exception) as raised:
            request_api = MockRequestsAPI(response=None)
            pannous_api = PannousAPI(request_api=request_api)
            response = pannous_api.ask_question("http://testurl", "Hello", "testid")
        self.assertEqual(raised.exception.args[0], "No response from pannous service")

    def test_ask_question_missing_text(self):

        with self.assertRaises(Exception) as raised:
            request_api = MockRequestsAPI()
            pannous_api = PannousAPI(request_api=request_api)
            request_api._response = json.loads("""
            {
                "output": [
                    { "actions": { "say": {"response": "Hello"} } }
                ]
            }
            """)
            response = pannous_api.ask_question("http://testurl", "Hello", "testid")
        self.assertEqual(raised.exception.args[0], "'text' section missing from output[0]['actions']['say'] in pannous json_data")

    def test_ask_question_missing_say(self):

        with self.assertRaises(Exception) as raised:
            request_api = MockRequestsAPI()
            pannous_api = PannousAPI(request_api=request_api)
            request_api._response = json.loads("""
            {
                "output": [
                    { "actions": { "said": {"response": "Hello"} } }
                ]
            }
            """)
            response = pannous_api.ask_question("http://testurl", "Hello", "testid")
        self.assertEqual(raised.exception.args[0], "'say' section missing from output[0]['actions'] in pannous json_data")

    def test_ask_question_missing_actions(self):

        with self.assertRaises(Exception) as raised:
            request_api = MockRequestsAPI()
            pannous_api = PannousAPI(request_api=request_api)
            request_api._response = json.loads("""
            {
                "output": [
                    { "items": { "say": {"response": "Hello"} } }
                ]
            }
            """)
            response = pannous_api.ask_question("http://testurl", "Hello", "testid")
        self.assertEqual(raised.exception.args[0], "'actions' section in output[0] in pannous json_data")

    def test_ask_question_empty_output(self):

        with self.assertRaises(Exception) as raised:
            request_api = MockRequestsAPI()
            pannous_api = PannousAPI(request_api=request_api)
            request_api._response = json.loads("""
            {
                "output": []
            }
            """)
            response = pannous_api.ask_question("http://testurl", "Hello", "testid")
        self.assertEqual(raised.exception.args[0], "'output' section has no elements in pannous json_data")

        with self.assertRaises(Exception) as raised:
            request_api = MockRequestsAPI()
            pannous_api = PannousAPI(request_api=request_api)
            request_api._response = json.loads("""
            {
                "output": null
            }
            """)
            response = pannous_api.ask_question("http://testurl", "Hello", "testid")
        self.assertEqual(raised.exception.args[0], "'output' section has no elements in pannous json_data")

    def test_ask_question_missing_output(self):

        with self.assertRaises(Exception) as raised:
            request_api = MockRequestsAPI()
            pannous_api = PannousAPI(request_api=request_api)
            request_api._response = json.loads("""
            {
                "result": [
                    { "items": { "say": {"response": "Hello"} } }
                ]
            }
            """)
            response = pannous_api.ask_question("http://testurl", "Hello", "testid")
        self.assertEqual(raised.exception.args[0], "'output' section missing from pannous json_data")


class TestBot:

    def __init__(self):
        self.license_keys = None


class MockPannousAPI(object):

    def __init__(self, response=None, throw_exception=False):
        self._throw_exception = throw_exception
        self._response = response

    def ask_question(self, url, question, login):
        if self._throw_exception is True:
            raise Exception(self._response)
        else:
            return self._response


class PannousServiceTests(unittest.TestCase):

    def setUp(self):
        self.bot = TestBot()
        self.bot.license_keys = LicenseKeys()
        self.bot.license_keys.load_license_key_file(os.path.dirname(__file__)+"/test.keys")

    def test_ask_question(self):

        config = BrainServiceConfiguration("pannous")
        config.set_parameter("url", "http://test.pandora.url")

        service = PannousService(config=config, api=MockPannousAPI(response="Test pannous response"))
        self.assertIsNotNone(service)

        response = service.ask_question(self.bot, "testid", "what is a cat")
        self.assertEquals("Test pannous response", response)

    def test_ask_question_no_url(self):

        config = BrainServiceConfiguration("pannous")

        with self.assertRaises(Exception) as raised:
            service = PannousService(config=config, api=MockPannousAPI(response="Test pannous response"))
            self.assertIsNotNone(service)

            response = service.ask_question(self.bot, "testid", "what is a cat")
            self.assertEquals("", response)

        self.assertEqual(raised.exception.args[0], "Undefined url parameter")

    def test_ask_question_no_license_key(self):

        self.bot = TestBot()
        self.bot.license_keys = LicenseKeys()

        config = BrainServiceConfiguration("pannous")
        config.set_parameter("url", "http://test.pandora.url")

        service = PannousService(config=config, api=MockPannousAPI(response="Test pannous response"))
        self.assertIsNotNone(service)

        response = service.ask_question(self.bot, "testid", "what is a cat")
        self.assertEquals("", response)

    def test_ask_question_with_exception(self):

        config = BrainServiceConfiguration("pannous")
        config.set_parameter("url", "http://test.pandora.url")

        service = PannousService(config=config, api=MockPannousAPI(response="Some wierd error", throw_exception=True))
        self.assertIsNotNone(service)

        response = service.ask_question(self.bot, "testid", "what is a cat")
        self.assertEquals("", response)

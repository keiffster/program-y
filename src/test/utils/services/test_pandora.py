import unittest
import os
from xml.etree import ElementTree

from programy.utils.license.keys import LicenseKeys
from programy.utils.services.pandora import PandoraService, PandoraAPI
from programy.utils.services.service import BrainServiceConfiguration
from test.utils.services.mock_requests import MockRequestsAPI

class PandoraAPITests(unittest.TestCase):

    def test_ask_question_valid_xml(self):

        request_api = MockRequestsAPI()
        pandora_api = PandoraAPI(request_api=request_api)
        request_api._response = """
        <response>
            <that>Hello</that>
        </response>
        """
        response = pandora_api.ask_question("http://testurl", "Hello", "testid")
        self.assertEquals(response, "Hello")

    def test_ask_question_no_response(self):

        with self.assertRaises(Exception) as raised:
            request_api = MockRequestsAPI(response=None)
            pandora_api = PandoraAPI(request_api=request_api)
            response = pandora_api.ask_question("http://testurl", "Hello", "testid")
        self.assertEqual(raised.exception.args[0], "No response from pandora service")

    def test_ask_question_no_that(self):

        request_api = MockRequestsAPI()
        pandora_api = PandoraAPI(request_api=request_api)
        request_api._response = """
        <response>
        </response>
        """

        with self.assertRaises(Exception) as raised:
            response = pandora_api.ask_question("http://testurl", "Hello", "testid")
        self.assertEqual(raised.exception.args[0], "Invalid response from pandora service, no <that> element in xml")

class TestBot:

    def __init__(self):
        self.license_keys = None


class MockPandoraAPI(object):

    def __init__(self, response=None, throw_exception=False):
        self._throw_exception = throw_exception
        self._response = response

    def ask_question(self, url, question, login):
        if self._throw_exception is True:
            raise Exception(self._response)
        else:
            return self._response


class PandoraServiceTests(unittest.TestCase):

    def setUp(self):
        self.bot = TestBot()
        self.bot.license_keys = LicenseKeys()
        self.bot.license_keys.load_license_key_file(os.path.dirname(__file__)+"/test.keys")

    def test_ask_question(self):

        config = BrainServiceConfiguration("pandora")
        config.set_parameter("url", "http://test.pandora.url")

        service = PandoraService(config=config, api=MockPandoraAPI(response="Test pandora response"))
        self.assertIsNotNone(service)

        response = service.ask_question(self.bot, "testid", "what is a cat")
        self.assertEquals("Test pandora response", response)

    def test_ask_question_no_url(self):

        config = BrainServiceConfiguration("pandora")

        with self.assertRaises(Exception) as raised:
            service = PandoraService(config=config, api=MockPandoraAPI(response="Test pandora response"))
            self.assertIsNotNone(service)

            response = service.ask_question(self.bot, "testid", "what is a cat")
            self.assertEquals("", response)

        self.assertEqual(raised.exception.args[0], "Undefined url parameter")

    def test_ask_question_no_botid(self):

        self.bot = TestBot()
        self.bot.license_keys = LicenseKeys()

        config = BrainServiceConfiguration("pandora")
        config.set_parameter("url", "http://test.pandora.url")

        service = PandoraService(config=config, api=MockPandoraAPI(response="Test pandora response"))
        self.assertIsNotNone(service)

        response = service.ask_question(self.bot, "testid", "what is a cat")
        self.assertEquals("", response)

    def test_ask_question_with_exception(self):

        config = BrainServiceConfiguration("pandora")
        config.set_parameter("url", "http://test.pandora.url")

        service = PandoraService(config=config, api=MockPandoraAPI(response="Some wierd error", throw_exception=True))
        self.assertIsNotNone(service)

        response = service.ask_question(self.bot, "testid", "what is a cat")
        self.assertEquals("", response)

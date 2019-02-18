import unittest
import os

from programy.services.pandora import PandoraService, PandoraAPI
from programy.services.service import BrainServiceConfiguration
from programytest.services.mock_requests import MockRequestsAPI

from programytest.client import TestClient


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
        self.assertEqual(response, "Hello")

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
        client = TestClient()
        client.add_license_keys_store()
        self._client_context = client.create_client_context("testid")

    def test_ask_question(self):

        config = BrainServiceConfiguration("pandora")
        config._url = "http://test.pandora.url"

        service = PandoraService(config=config, api=MockPandoraAPI(response="Test pandora response"))
        self.assertIsNotNone(service)

        response = service.ask_question(self._client_context, "what is a cat")
        self.assertEqual("Test pandora response", response)

    def test_ask_question_no_url(self):

        config = BrainServiceConfiguration("pandora")

        with self.assertRaises(Exception) as raised:
            service = PandoraService(config=config, api=MockPandoraAPI(response="Test pandora response"))
            self.assertIsNotNone(service)

            response = service.ask_question(self._client_context, "what is a cat")
            self.assertEqual("", response)

        self.assertEqual(raised.exception.args[0], "Undefined url parameter")

    def test_ask_question_no_botid(self):

        self._client_context.client.license_keys._keys.clear()

        config = BrainServiceConfiguration("pandora")
        config._url = "http://test.pandora.url"

        service = PandoraService(config=config, api=MockPandoraAPI(response="Test pandora response"))
        self.assertIsNotNone(service)

        response = service.ask_question(self._client_context, "what is a cat")
        self.assertEqual("", response)

    def test_ask_question_with_exception(self):

        config = BrainServiceConfiguration("pandora")
        config._url = "http://test.pandora.url"

        service = PandoraService(config=config, api=MockPandoraAPI(response="Some wierd error", throw_exception=True))
        self.assertIsNotNone(service)

        response = service.ask_question(self._client_context, "what is a cat")
        self.assertEqual("", response)

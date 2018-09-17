import unittest
import os

from programy.services.duckduckgo import DuckDuckGoService
from programy.services.duckduckgo import DuckDuckGoAPI
from programy.services.requestsapi import RequestsAPI
from programy.services.service import BrainServiceConfiguration

from programytest.client import TestClient


class MockResponse(object):

    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text


class MockRequestsAPI(object):

    def __init__(self):
        self._status_code = None
        self._response = None

    def get(self, url, params):
        self._url = url
        return MockResponse(self._status_code, self._response)


class MockDuckDuckGoAPI(object):

    def __init__(self, response=None, throw_exception=False):
        self._response = response
        self._throw_exception = throw_exception

    def ask_question(self, url, question):
        self._question = question
        self._url = url
        if self._throw_exception is True:
            raise Exception()
        else:
            return self._response


class TestDuckDuckGoAPI(unittest.TestCase):

    def test_init_no_requestapi(self):
        api = DuckDuckGoAPI()
        self.assertIsNotNone(api)
        self.assertIsInstance(api._requests_api, RequestsAPI)

    def test_init_with_requestapi(self):
        api = DuckDuckGoAPI(MockRequestsAPI())
        self.assertIsNotNone(api)
        self.assertIsInstance(api._requests_api, MockRequestsAPI)

    def test_ask_question(self):
        request_api = MockRequestsAPI()
        api = DuckDuckGoAPI(request_api)
        self.assertIsNotNone(api)
        self.assertIsInstance(api._requests_api, MockRequestsAPI)

        request_api._status_code = 200
        request_api._response = b'{"RelatedTopics": [{"Text": "A feline, 4 legged thing"}]}'

        response = api.ask_question("http:/test.url.com/ask", "cat")

        self.assertEqual("A feline, 4 legged thing", response)


class DuckDuckGoServiceTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        client.add_license_keys_store()
        self._client_context = client.create_client_context("testid")

    def test_init_with_no_request_api(self):
        config = BrainServiceConfiguration("pannous")
        config._url = "http://test.pandora.url"

        service = DuckDuckGoService(config=config)

        self.assertIsNotNone(service)
        self.assertIsInstance(service._api, DuckDuckGoAPI)

    def test_init_with_no_url(self):
        config = BrainServiceConfiguration("pannous")
        config._url = None

        with self.assertRaises(Exception):
            service = DuckDuckGoService(config=config)

    def test_ask_question(self):

        config = BrainServiceConfiguration("pannous")
        config._url = "http://test.pandora.url"

        service = DuckDuckGoService(config=config, api=MockDuckDuckGoAPI(response="Test DuckDuckGo response"))
        self.assertIsNotNone(service)

        response = service.ask_question(self._client_context, "what is a cat")
        self.assertEqual("Test DuckDuckGo response", response)

    def test_ask_question_general_exception(self):
        config = BrainServiceConfiguration("pannous")
        config._url = "http://test.pandora.url"

        service = DuckDuckGoService(config=config, api=MockDuckDuckGoAPI(response=None, throw_exception=True))
        self.assertIsNotNone(service)

        response = service.ask_question(self._client_context, "what is a cat")
        self.assertEqual("", response)


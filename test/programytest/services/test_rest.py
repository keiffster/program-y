import unittest

from programy.services.rest import GenericRESTService, RestAPI
from programy.services.service import BrainServiceConfiguration

from programytest.client import TestClient


class MockRestResponse(object):
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text


class MockRestAPI(object):

    def __init__(self, status_code=200, response="REST response"):
        self.status_code = status_code
        self.response = response

    def get(self, host):
        return MockRestResponse(self.status_code, self.response)

    def post(self, host, data):
        return MockRestResponse(self.status_code, self.response)


class RestServiceTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        client.add_license_keys_store()
        self._client_context = client.create_client_context("testid")

    def test_init_default_api(self):
        config = BrainServiceConfiguration("rest")
        config._host = "127.0.0.1"
        config._method = "GET"

        service = GenericRESTService(config=config)
        self.assertIsNotNone(service)
        self.assertIsInstance(service.api, RestAPI)

    def test_ask_default_method(self):
        config = BrainServiceConfiguration("rest")
        config._host = "127.0.0.1"

        service = GenericRESTService(config=config)
        self.assertIsNotNone(service)
        self.assertEqual(service.method, "GET")

    def test_ask_question_get(self):
        config = BrainServiceConfiguration("rest")
        config._host = "127.0.0.1"
        config._method = "GET"

        service = GenericRESTService(config=config, api=MockRestAPI(200, "Test REST response"))
        self.assertIsNotNone(service)

        response = service.ask_question(self._client_context, "what is a cat")
        self.assertEqual("Test REST response", response)

    def test_ask_question_post(self):
        config = BrainServiceConfiguration("rest")
        config._host = "127.0.0.1"
        config._method = "POST"

        service = GenericRESTService(config=config, api=MockRestAPI(200, "Post REST response"))
        self.assertIsNotNone(service)

        response = service.ask_question(self._client_context, "what is a cat")
        self.assertEqual("Post REST response", response)

    def test_ask_question_delete(self):
        config = BrainServiceConfiguration("rest")
        config._host = "127.0.0.1"
        config._method = "DELETE"

        service = GenericRESTService(config=config, api=MockRestAPI())
        self.assertIsNotNone(service)

        self.assertEqual("", service.ask_question(self._client_context, "what is a cat"))

    def test_ask_question_error(self):
        config = BrainServiceConfiguration("rest")
        config._host = "127.0.0.1"
        config._method = "GET"

        service = GenericRESTService(config=config, api=MockRestAPI(500, "Bad thing happened!"))
        self.assertIsNotNone(service)

        self.assertEqual("", service.ask_question(self._client_context, "what is a cat"))

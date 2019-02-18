import unittest

from programy.services.programy import ProgramyRESTService
from programy.config.brain.service import BrainServiceConfiguration

from programytest.client import TestClient


class ProgramyRESTServiceTests(unittest.TestCase):

    def test_format_payload(self):
        client = TestClient()
        client_context = client.create_client_context("testid")

        config = BrainServiceConfiguration("rest")
        config._classname = "programy.testclass"
        config._method = "GET"
        config._host = "localhost"
        config._port = 8080
        config._url = "/api/v1.0/ask"

        service = ProgramyRESTService(config, api=None)
        self.assertEqual({'question': 'Hello', 'userid': 'testid'}, service._format_payload(client_context, "Hello"))

    def test_format_get_url(self):
        client = TestClient()
        client_context = client.create_client_context("testid")

        config = BrainServiceConfiguration("rest")
        config._classname = "programy.testclass"
        config._method = "GET"
        config._host = "localhost"
        config._port = 8080
        config._url = "/api/v1.0/ask"

        service = ProgramyRESTService(config, api=None)
        self.assertEqual("/api/v1.0/ask?question=Hello&userid=testid", service._format_get_url("/api/v1.0/ask", client_context, "Hello"))

    def test_parse_response(self):
        client = TestClient()
        client_context = client.create_client_context("testid")

        config = BrainServiceConfiguration("rest")
        config._classname = "programy.testclass"
        config._method = "GET"
        config._host = "localhost"
        config._port = 8080
        config._url = "/api/v1.0/ask"

        service = ProgramyRESTService(config, api=None)
        self.assertEqual("Hello", service._parse_response('[{"response": {"answer": "Hello"}}]'))
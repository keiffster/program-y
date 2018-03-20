import unittest
import os

from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient


class RequestTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(RequestTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files = [os.path.dirname(__file__)]


class RequestAIMLTests(unittest.TestCase):

    def setUp(self):
        client = RequestTestClient()
        self._client_context = client.create_client_context("testid")

    def test_request(self):
        Request = self._client_context.bot.ask_question(self._client_context, "HELLO")
        self.assertIsNotNone(Request)
        self.assertEquals(Request, "Hi! It's delightful to see you.")

        Request = self._client_context.bot.ask_question(self._client_context, "WHAT DID I SAY")
        self.assertIsNotNone(Request)
        self.assertEquals(Request, "You said, HELLO")

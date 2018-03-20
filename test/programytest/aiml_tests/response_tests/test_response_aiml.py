import unittest
import os

from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient


class ResponseTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(ResponseTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files = [os.path.dirname(__file__)]


class ResponseAIMLTests(unittest.TestCase):

    def setUp(self):
        client = ResponseTestClient()
        self._client_context = client.create_client_context("testid")

    def test_Response(self):
        response = self._client_context.bot.ask_question(self._client_context, "HELLO")
        self.assertIsNotNone(response)
        self.assertEquals(response, "Hi! It's delightful to see you.")

        response = self._client_context.bot.ask_question(self._client_context, "CAN YOU REPEAT THAT")
        self.assertIsNotNone(response)
        self.assertEquals(response, "I said, Hi! It's delightful to see you.")

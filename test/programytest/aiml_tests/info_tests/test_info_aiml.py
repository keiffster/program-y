import unittest
import os

from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient

class InfoAIMLTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(InfoAIMLTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files = [os.path.dirname(__file__)]


class InfoAIMLTests(unittest.TestCase):

    def setUp(self):
        client = InfoAIMLTestClient()
        self._client_context = client.create_client_context("testid")

    def test_program(self):
        response = self._client_context.bot.ask_question(self._client_context,  "TEST PROGRAM")
        self.assertIsNotNone(response)
        self.assertEqual(response, "AIMLBot")

    def test_id(self):
        response = self._client_context.bot.ask_question(self._client_context, "TEST ID")
        self.assertIsNotNone(response)
        self.assertEqual(response, "testclient")

    def test_env(self):

        self._client_context.bot.brain.properties.add_property("env", "test")

        response = self._client_context.bot.ask_question(self._client_context, "TEST ENVIRONMENT")
        self.assertIsNotNone(response)
        self.assertEqual(response, "ENVIRONMENT IS test")

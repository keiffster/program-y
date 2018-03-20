import unittest
import os

from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient


class ThinkTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(ThinkTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files = [os.path.dirname(__file__)]


class ThinkAIMLTests(unittest.TestCase):

    def setUp(self):
        client = ThinkTestClient()
        self._client_context = client.create_client_context("testid")

    def test_think(self):
        response = self._client_context.bot.ask_question(self._client_context,  "THINK")
        self.assertIsNotNone(response)
        self.assertEqual(response, "")

    def test_set_think(self):
        response = self._client_context.bot.ask_question(self._client_context, "SET THINK")
        self.assertIsNotNone(response)
        self.assertEqual(response, "")

        self.assertEquals("Keith", self._client_context.bot.get_conversation(self._client_context).current_question().property("name"))

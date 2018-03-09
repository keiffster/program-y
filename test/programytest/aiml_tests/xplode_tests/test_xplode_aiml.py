import unittest
import os

from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient


class BasicTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(BasicTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files = [os.path.dirname(__file__)]


class XPlodeAIMLTests(unittest.TestCase):

    def setUp(self):
        self._client_context = ClientContext(BasicTestClient(), "testid")
        self._client_context.bot = self._client_context.client.bot
        self._client_context.brain = self._client_context.bot.brain

    def test_explode(self):
        response = self._client_context.bot.ask_question(self._client_context,  "MAKE EXPLODE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "h e l l o w o r l d")

    def test_implode(self):
        response = self._client_context.bot.ask_question(self._client_context, "MAKE IMPLODE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "helloworld")

    def test_nested_explode_implode(self):
        response = self._client_context.bot.ask_question(self._client_context, "NESTED EXPLODE IMPLODE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "helloworld")

    def test_nested_implode_explode(self):
        response = self._client_context.bot.ask_question(self._client_context, "NESTED IMPLODE EXPLODE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "h e l l o w o r l d")

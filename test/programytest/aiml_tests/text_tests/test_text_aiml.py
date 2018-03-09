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


class TextAIMLTests(unittest.TestCase):

    def setUp(self):
        self._client_context = ClientContext(BasicTestClient(), "testid")
        self._client_context.bot = self._client_context.client.bot
        self._client_context.brain = self._client_context.bot.brain

    def test_lowercase(self):
        response = self._client_context.bot.ask_question(self._client_context,  "MAKE LOWERCASE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "hello world")

    def test_uppercase(self):
        response = self._client_context.bot.ask_question(self._client_context, "MAKE UPPERCASE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "HELLO WORLD")


    def test_sentence(self):
        response = self._client_context.bot.ask_question(self._client_context, "MAKE SENTENCE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Hello world")


    def test_formal(self):
        response = self._client_context.bot.ask_question(self._client_context, "MAKE FORMAL")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Hello World")


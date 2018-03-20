import unittest
import os

from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient


class VobaularyTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(VobaularyTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files = [os.path.dirname(__file__)]


class VocabularyAIMLTests(unittest.TestCase):

    def setUp(self):
        client = VobaularyTestClient()
        self._client_context = client.create_client_context("testid")

    def test_vocabulary(self):
        response = self._client_context.bot.ask_question(self._client_context,  "TEST VOCABULARY")
        self.assertIsNotNone(response)
        self.assertEqual(response, "My vocabulary is 3 words")

    def test_size(self):
        response = self._client_context.bot.ask_question(self._client_context, "TEST SIZE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "I can answer 2 questions")

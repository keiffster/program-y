import unittest
import os

from programytest.client import TestClient


class VobaularyTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(VobaularyTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class VocabularyAIMLTests(unittest.TestCase):

    def setUp(self):
        client = VobaularyTestClient()
        self._client_context = client.create_client_context("testid")

    def test_vocabulary(self):
        response = self._client_context.bot.ask_question(self._client_context,  "TEST VOCABULARY")
        self.assertIsNotNone(response)
        self.assertEqual(response, "My vocabulary is 3 words.")

    def test_size(self):
        response = self._client_context.bot.ask_question(self._client_context, "TEST SIZE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "I can answer 2 questions.")

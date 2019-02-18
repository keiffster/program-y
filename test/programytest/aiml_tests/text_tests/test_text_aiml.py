import unittest
import os

from programytest.client import TestClient


class TextTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(TextTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class TextAIMLTests(unittest.TestCase):

    def setUp(self):
        client = TextTestClient()
        self._client_context = client.create_client_context("testid")

    def test_lowercase(self):
        response = self._client_context.bot.ask_question(self._client_context,  "MAKE LOWERCASE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Hello world.")

    def test_uppercase(self):
        response = self._client_context.bot.ask_question(self._client_context, "MAKE UPPERCASE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "HELLO WORLD.")


    def test_sentence(self):
        response = self._client_context.bot.ask_question(self._client_context, "MAKE SENTENCE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Hello world.")


    def test_formal(self):
        response = self._client_context.bot.ask_question(self._client_context, "MAKE FORMAL")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Hello World.")


import unittest
import os

from programytest.client import TestClient


class ExplodeTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(ExplodeTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class ExlodeAIMLTests(unittest.TestCase):

    def setUp(self):
        client = ExplodeTestClient()
        self._client_context = client.create_client_context("testid")

    def test_explode(self):
        response = self._client_context.bot.ask_question(self._client_context,  "MAKE EXPLODE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "H e l l o w o r l d.")

    def test_implode(self):
        response = self._client_context.bot.ask_question(self._client_context, "MAKE IMPLODE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Helloworld.")

    def test_nested_explode_implode(self):
        response = self._client_context.bot.ask_question(self._client_context, "NESTED EXPLODE IMPLODE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Helloworld.")

    def test_nested_implode_explode(self):
        response = self._client_context.bot.ask_question(self._client_context, "NESTED IMPLODE EXPLODE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "H e l l o w o r l d.")

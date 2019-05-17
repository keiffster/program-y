import unittest
import os

from programytest.client import TestClient

class InputAIMLTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(InputAIMLTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class InputAIMLTests(unittest.TestCase):

    def setUp(self):
        client = InputAIMLTestClient()
        self._client_context = client.create_client_context("testid")

    def test_basic_input(self):
        response = self._client_context.bot.ask_question(self._client_context,  "TEST INPUT")
        self.assertIsNotNone(response)
        self.assertEqual(response, "TEST INPUT.")

    def test_basic_series(self):
        response = self._client_context.bot.ask_question(self._client_context,  "QUESTION 1")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Hello 1.")

        response = self._client_context.bot.ask_question(self._client_context,  "QUESTION 2")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Hello 2.")

        response = self._client_context.bot.ask_question(self._client_context,  "PREVIOUS QUESTION")
        self.assertIsNotNone(response)
        self.assertEqual(response, "QUESTION 1.")

        response = self._client_context.bot.ask_question(self._client_context,  "2ND PREVIOUS QUESTION")
        self.assertIsNotNone(response)
        self.assertEqual(response, "PREVIOUS QUESTION.")

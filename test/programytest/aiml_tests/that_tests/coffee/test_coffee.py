import unittest
import os

from programytest.client import TestClient


class ThatTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(ThatTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class ThatAIMLTests(unittest.TestCase):

    def setUp(self):
        client = ThatTestClient()
        self._client_context = client.create_client_context("testid")

    def test_coffee_yes_question(self):
        response = self._client_context.bot.ask_question(self._client_context, "I LIKE COFFEE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'DO YOU TAKE CREAM OR SUGAR IN YOUR COFFEE?')

        response = self._client_context.bot.ask_question(self._client_context, "YES")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'I DO TOO.')

    def test_coffee_no_question(self):
        response = self._client_context.bot.ask_question(self._client_context, "I LIKE COFFEE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'DO YOU TAKE CREAM OR SUGAR IN YOUR COFFEE?')

        response = self._client_context.bot.ask_question(self._client_context, "NO")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'REALLY? I HAVE A HARD TIME DRINKING BLACK COFFEE.')

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

    def test_multiple_sentenes(self):
        response = self._client_context.bot.ask_question(self._client_context, "START")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'This is sentence 1. This is sentence two.')

        response = self._client_context.bot.ask_question(self._client_context, "CONTINUE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'TEST PASS.')


import unittest
import os

from programytest.client import TestClient


class ResponseTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(ResponseTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class ResponseAIMLTests(unittest.TestCase):

    def setUp(self):
        client = ResponseTestClient()
        self._client_context = client.create_client_context("testid")

    def test_Response(self):
        response = self._client_context.bot.ask_question(self._client_context, "HELLO")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Hi! It's delightful to see you.")

        response = self._client_context.bot.ask_question(self._client_context, "CAN YOU REPEAT THAT")
        self.assertIsNotNone(response)
        self.assertEqual(response, "I said, Hi! It's delightful to see you.")

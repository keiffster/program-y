import unittest
import os

from programytest.client import TestClient


class RequestTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(RequestTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class RequestAIMLTests(unittest.TestCase):

    def setUp(self):
        client = RequestTestClient()
        self._client_context = client.create_client_context("testid")

    def test_request(self):
        Request = self._client_context.bot.ask_question(self._client_context, "HELLO")
        self.assertIsNotNone(Request)
        self.assertEqual(Request, "Hi! It's delightful to see you.")

        Request = self._client_context.bot.ask_question(self._client_context, "WHAT DID I SAY")
        self.assertIsNotNone(Request)
        self.assertEqual(Request, "You said, HELLO.")

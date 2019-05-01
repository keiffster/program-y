import unittest
import os

from programytest.client import TestClient


class WildcardTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(WildcardTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class WildcardAIMLTests(unittest.TestCase):

    def setUp(self):
        client = WildcardTestClient()
        self._client_context = client.create_client_context("testid")

    def test_gianfrasoft_196(self):
        response = self._client_context.bot.ask_question(self._client_context,  "HELLO TEST1")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HELLO RESULT1.')

        response = self._client_context.bot.ask_question(self._client_context,  "HELLO TEST2")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HELLO RESULT2.')

        response = self._client_context.bot.ask_question(self._client_context,  "HELLO TEST2 THERE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HELLO RESULT3 THERE.')


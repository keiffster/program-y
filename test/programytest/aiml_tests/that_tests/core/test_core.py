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

    def test_that_single_that_word(self):
        response = self._client_context.bot.ask_question(self._client_context, "HELLO")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HI THERE.')

        response = self._client_context.bot.ask_question(self._client_context, "HELLO AGAIN")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HELLO WITH THAT.')

    def test_wildcard_matching_one_or_more(self):
        response = self._client_context.bot.ask_question(self._client_context, "WELCOME")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Aaa bbb ccc ddd.')

        response = self._client_context.bot.ask_question(self._client_context, "AND AGAIN")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Matched.')

    def test_wildcard_matching_zero_or_more(self):
        response = self._client_context.bot.ask_question(self._client_context, "WELCOME2")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Xxx yyy zzz.')

        response = self._client_context.bot.ask_question(self._client_context, "AND AGAIN")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Matched2.')

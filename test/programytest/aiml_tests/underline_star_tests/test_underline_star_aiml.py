import unittest
import os

from programytest.client import TestClient


class UnderlineStarTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(UnderlineStarTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class UnderlineStarAIMLTests(unittest.TestCase):

    def setUp(self):
        client = UnderlineStarTestClient()
        self._client_context = client.create_client_context("testid")

    def test_underline_first(self):
        response = self._client_context.bot.ask_question(self._client_context,  "SAY HEY")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'UNDERLINE IS SAY.')

    def test_underline_last(self):
        response = self._client_context.bot.ask_question(self._client_context, "HELLO THERE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'UNDERLINE IS THERE.')

    def test_underline_middle(self):
        response = self._client_context.bot.ask_question(self._client_context, "HI KEIFF MATE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'UNDERLINE IS KEIFF.')

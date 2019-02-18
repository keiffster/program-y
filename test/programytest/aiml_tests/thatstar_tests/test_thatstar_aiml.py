import unittest
import os

from programytest.client import TestClient


class ThatStarTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(ThatStarTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class ThatStarAIMLTests(unittest.TestCase):

    def setUp(self):
        client = ThatStarTestClient()
        self._client_context = client.create_client_context("testid")

    def test_single_thatstar_word_default(self):
        # We need to ask 2 questions, first we get a response which is stored in the <that> clause, we then return it
        # on the second question

        response = self._client_context.bot.ask_question(self._client_context, "HELLO THERE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HI THERE.')

        response = self._client_context.bot.ask_question(self._client_context, "I SAID HI THERE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HEARD YOU SAY HI THERE.')

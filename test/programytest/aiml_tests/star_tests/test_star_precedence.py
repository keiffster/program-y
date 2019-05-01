import unittest
import os

from programytest.client import TestClient


class StarPrecedenceTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(StarPrecedenceTestClient, self).load_storage()
        self.add_default_stores()
        self.add_single_categories_store(os.path.dirname(__file__) + os.sep + "precedence.aiml")


class StarPrecedenceAIMLTests(unittest.TestCase):

    def setUp(self):
        client =StarPrecedenceTestClient()
        self._client_context = client.create_client_context("testid")

    def test_star_precedence(self):
        response = self._client_context.bot.ask_question(self._client_context,  "FIRSTWORD")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'FOUND1.')

        response = self._client_context.bot.ask_question(self._client_context,  "SECONDWORD")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'NOTHING FOUND.')

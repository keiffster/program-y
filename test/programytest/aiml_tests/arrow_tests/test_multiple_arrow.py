import unittest
import os

from programytest.client import TestClient


class MultipleArrowsTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(MultipleArrowsTestClient, self).load_storage()
        self.add_default_stores()
        self.add_single_categories_store(os.path.dirname(__file__) + os.sep + "multiple_arrows.aiml")


class MultipleArrowsAIMLTests(unittest.TestCase):

    def setUp(self):
        client = MultipleArrowsTestClient()
        self._client_context = client.create_client_context("testid")

    def test_multiple_arrows_no_priority(self):
        response = self._client_context.bot.ask_question(self._client_context,  "ASEPARATOR ADEBUG1 ADEBUG2")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'AFOUND2.')

        response = self._client_context.bot.ask_question(self._client_context,  "ADEBUG1 ADEBUG2")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'AFOUND1.')

    def test_multiple_arrows_with_priority(self):
        response = self._client_context.bot.ask_question(self._client_context,  "BSEPARATOR BDEBUG1 BDEBUG2")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'BFOUND2.')

        response = self._client_context.bot.ask_question(self._client_context,  "BDEBUG1 BDEBUG2")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'BFOUND1.')

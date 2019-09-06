import unittest
import os

from programytest.client import TestClient


class SynsetsTestsClient(TestClient):

    def __init__(self):
        TestClient.__init__(self, debug=True)

    def load_storage(self):
        super(SynsetsTestsClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class WordNetAIMLTests(unittest.TestCase):

    def setUp (self):
        client = SynsetsTestsClient()
        self._client_context = client.create_client_context("testid")

    def test_wordnet_definition(self):
        response = self._client_context.bot.ask_question(self._client_context, "WORDNET CAT")
        self.assertIsNotNone(response)
        self.assertEqual("Feline mammal usually having thick soft fur and no ability to roar: domestic cats; wildcats.", response)

    def test_wordnet_no_definition(self):
        response = self._client_context.bot.ask_question(self._client_context, "WORDNET KJGJHGJJG")
        self.assertIsNotNone(response)
        self.assertEqual("", response)

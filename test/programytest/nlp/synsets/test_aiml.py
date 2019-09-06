import unittest
import os

from programytest.client import TestClient


class SynsetAIMLTestsClient(TestClient):

    def __init__(self):
        TestClient.__init__(self, debug=True)

    def load_storage(self):
        super(SynsetAIMLTestsClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class SynsetAIMLTests(unittest.TestCase):

    def setUp (self):
        client = SynsetAIMLTestsClient()
        self._client_context = client.create_client_context("testid")

    def test_synset(self):
        response = self._client_context.bot.ask_question(self._client_context, "SYNSETS SIMILAR HACK CHOP")
        self.assertIsNotNone(response)
        self.assertEqual("TRUE.", response)

        response = self._client_context.bot.ask_question(self._client_context, "SYNSETS SIMILAR OCTOPUS SHRUMP")
        self.assertIsNotNone(response)
        self.assertEqual("FALSE.", response)
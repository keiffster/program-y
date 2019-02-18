import unittest
import os

from programytest.client import TestClient


class NormalizeTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(NormalizeTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])
        self.add_normal_store(os.path.dirname(__file__)+ os.sep + "normal.txt")


class NormalizeAIMLTests(unittest.TestCase):

    def setUp(self):
        client = NormalizeTestClient()
        self._client_context = client.create_client_context("testid")

    def test_normalize(self):
        response = self._client_context.bot.ask_question(self._client_context,  "TEST NORMALIZE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Keithsterling dot com.")

    def test_normalize_star(self):
        response = self._client_context.bot.ask_question(self._client_context,  "NORMALIZE test.org", srai=True)
        self.assertIsNotNone(response)
        self.assertEqual(response, "Test dot org")

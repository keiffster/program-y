import unittest
import os

from programytest.client import TestClient


class RegexTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(RegexTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class RegexAIMLTests(unittest.TestCase):

    def setUp(self):
        client = RegexTestClient()
        self._client_context = client.create_client_context("testid")

    def test_regex(self):
        response = self._client_context.bot.ask_question(self._client_context, "I AM LEGION")
        self.assertIsNotNone(response)
        self.assertEquals(response, "Hello Legion.")

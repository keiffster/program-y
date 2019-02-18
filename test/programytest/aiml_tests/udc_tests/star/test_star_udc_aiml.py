import unittest
import os

from programytest.client import TestClient


class StarUDCTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(StarUDCTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class StarUDCAIMLTests(unittest.TestCase):

    def setUp(self):
        client = StarUDCTestClient()
        self._client_context = client.create_client_context("testid")

    def test_udc_multi_word_question(self):
        response = self._client_context.bot.ask_question(self._client_context, "Ask Question")
        self.assertIsNotNone(response)
        self.assertEqual(response, "UDC Star Response.")

    def test_udc_single_word_question(self):
        response = self._client_context.bot.ask_question(self._client_context, "Question")
        self.assertIsNotNone(response)
        self.assertEqual(response, "UDC Star Response.")

    def test_udc_empty_string_question(self):
        response = self._client_context.bot.ask_question(self._client_context, "")
        self.assertIsNotNone(response)
        self.assertEqual(response, "")

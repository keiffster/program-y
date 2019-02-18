import unittest
import os

from programytest.client import TestClient


class HashUDCTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(HashUDCTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])

    def load_configuration(self, arguments):
        super(HashUDCTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0]._empty_string = "YEMPTY"
        


class UDCAIMLTests(unittest.TestCase):

    def setUp(self):
        client = HashUDCTestClient()
        self._client_context = client.create_client_context("testid")

    def test_udc_multi_word_question(self):
        response = self._client_context.bot.ask_question(self._client_context, "Ask Question")
        self.assertIsNotNone(response)
        self.assertEqual(response, "UDC Hash Response.")

    def test_udc_single_word_question(self):
        response = self._client_context.bot.ask_question(self._client_context, "Question")
        self.assertIsNotNone(response)
        self.assertEqual(response, "UDC Hash Response.")

    def test_udc_empty_string_question1(self):
        response = self._client_context.bot.ask_question(self._client_context, "YEMPTY")
        self.assertIsNotNone(response)
        self.assertEqual(response, "UDC Hash Response.")

    def test_udc_empty_string_question2(self):
        response = self._client_context.bot.ask_question(self._client_context, "")
        self.assertIsNotNone(response)
        self.assertEqual(response, "UDC Hash Response.")

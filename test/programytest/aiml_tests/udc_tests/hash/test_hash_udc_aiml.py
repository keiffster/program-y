import unittest
import os

from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient


class HashUDCTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(HashUDCTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._file = os.path.dirname(__file__)+os.sep+'hash_udc.aiml'
        self.configuration.client_configuration.configurations[0]._empty_string = "YEMPTY"


class UDCAIMLTests(unittest.TestCase):

    def setUp(self):
        client = HashUDCTestClient()
        self._client_context = client.create_client_context("testid")

    def test_udc_multi_word_question(self):
        response = self._client_context.bot.ask_question(self._client_context, "Ask Question")
        self.assertIsNotNone(response)
        self.assertEqual(response, "UDC Hash Response")

    def test_udc_single_word_question(self):
        response = self._client_context.bot.ask_question(self._client_context, "Question")
        self.assertIsNotNone(response)
        self.assertEqual(response, "UDC Hash Response")

    def test_udc_empty_string_question1(self):
        response = self._client_context.bot.ask_question(self._client_context, "YEMPTY")
        self.assertIsNotNone(response)
        self.assertEqual(response, "UDC Hash Response")

    def test_udc_empty_string_question2(self):
        response = self._client_context.bot.ask_question(self._client_context, "")
        self.assertIsNotNone(response)
        self.assertEqual(response, "UDC Hash Response")

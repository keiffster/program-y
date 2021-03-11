import os
import unittest

from programytest.client import TestClient


class ArrowUDCTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(ArrowUDCTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])

    def load_configuration(self, arguments):
        super(ArrowUDCTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0]._empty_string = "YEMPTY"
        

class UDCAIMLTests(unittest.TestCase):

    def setUp(self):
        client = ArrowUDCTestClient()
        self._client_context = client.create_client_context("testid")

    def test_udc_has_this_question(self):
        response = self._client_context.bot.ask_question(self._client_context, "arrow this")
        self.assertIsNotNone(response)
        self.assertEqual(response, "UDC This Response.")

    def test_udc_that_arrow_question(self):
        response = self._client_context.bot.ask_question(self._client_context, "that")
        self.assertIsNotNone(response)
        self.assertEqual(response, "UDC That Response.")

    def test_udc_the_arrow_other_question(self):
        response = self._client_context.bot.ask_question(self._client_context, "THE arrow OTHER")
        self.assertIsNotNone(response)
        self.assertEqual(response, "UDC THE OTHER Response.")

    def test_udc_yempty_question(self):
        response = self._client_context.bot.ask_question(self._client_context, "YEMPTY")
        self.assertIsNotNone(response)
        self.assertEqual(response, "UDC YEMPTY Response.")

    def test_udc_other_question(self):
        response = self._client_context.bot.ask_question(self._client_context, "OTHER")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Arrow Empty Response.")

    def test_udc_empty_question(self):
        response = self._client_context.bot.ask_question(self._client_context, "")
        self.assertIsNotNone(response)
        self.assertEqual(response, "UDC YEMPTY Response.")

    def test_udc_space_question(self):
        response = self._client_context.bot.ask_question(self._client_context, " ")
        self.assertIsNotNone(response)
        self.assertEqual(response, "UDC YEMPTY Response.")

import os
import unittest

from programytest.client import TestClient


class StarUDCTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(StarUDCTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])

    def load_configuration(self, arguments):
        super(StarUDCTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0]._empty_string = "YEMPTY"


class StarUDCAIMLTests(unittest.TestCase):

    def setUp(self):
        client = StarUDCTestClient()
        self._client_context = client.create_client_context("testid")

    def test_star_this_question(self):
        response = self._client_context.bot.ask_question(self._client_context, "Ask THIS")
        self.assertIsNotNone(response)
        self.assertEqual(response, "UDC This Response.")

    def test_that_star_question(self):
        response = self._client_context.bot.ask_question(self._client_context, "That ASK")
        self.assertIsNotNone(response)
        self.assertEqual(response, "UDC That Response.")

    def test_the_star_other_question(self):
        response = self._client_context.bot.ask_question(self._client_context, "The Question Other")
        self.assertIsNotNone(response)
        self.assertEqual(response, "UDC THE OTHER Response.")

    def test_udc_something_question(self):
        response = self._client_context.bot.ask_question(self._client_context, "Something")
        self.assertIsNotNone(response)
        self.assertEqual(response, "UDC Star Response.")

    def test_udc_yempty_string_question(self):
        response = self._client_context.bot.ask_question(self._client_context, "YEMPTY")
        self.assertIsNotNone(response)
        self.assertEqual(response, "UDC YEMPTY Response.")

    def test_udc_empty_string_question(self):
        response = self._client_context.bot.ask_question(self._client_context, "")
        self.assertIsNotNone(response)
        self.assertEqual(response, "UDC YEMPTY Response.")

    def test_udc_space_string_question(self):
        response = self._client_context.bot.ask_question(self._client_context, "")
        self.assertIsNotNone(response)
        self.assertEqual(response, "UDC YEMPTY Response.")

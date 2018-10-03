import unittest
import os

from programytest.client import TestClient

class InfoAIMLTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(InfoAIMLTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class InfoAIMLTests(unittest.TestCase):

    def setUp(self):
        client = InfoAIMLTestClient()
        self._client_context = client.create_client_context("testid")

    def test_program(self):
        response = self._client_context.bot.ask_question(self._client_context,  "TEST PROGRAM")
        self.assertIsNotNone(response)
        self.assertEqual(response, "AIMLBot.")

    def test_id(self):
        response = self._client_context.bot.ask_question(self._client_context, "TEST ID")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Testclient.")

    def test_env(self):

        self._client_context.bot.brain.properties.add_property("env", "test")

        response = self._client_context.bot.ask_question(self._client_context, "TEST ENVIRONMENT")
        self.assertIsNotNone(response)
        self.assertEqual(response, "ENVIRONMENT IS test.")

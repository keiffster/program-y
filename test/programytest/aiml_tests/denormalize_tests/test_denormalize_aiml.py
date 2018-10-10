import unittest
import os

from programytest.client import TestClient

class DenormalizeAIMLTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(DenormalizeAIMLTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])
        self.add_denormal_store(os.path.dirname(__file__)+ os.sep + "denormal.txt")


class DenormalizeAIMLTests(unittest.TestCase):

    def setUp(self):
        client = DenormalizeAIMLTestClient()
        self._client_context = client.create_client_context("testid")

    def test_denormalize(self):
        response = self._client_context.bot.ask_question(self._client_context,  "TEST DENORMALIZE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Keithsterling.com.")

    def test_newdev7_say(self):
        response = self._client_context.bot.ask_question(self._client_context,  "SAY abc dot com")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Abc.com.")

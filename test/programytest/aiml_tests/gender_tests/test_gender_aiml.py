import unittest
import os

from programytest.client import TestClient

class GenderAIMLTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(GenderAIMLTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])
        self.add_gender_store(os.path.dirname(__file__)+ os.sep + "gender.txt")


class GenderAIMLTests(unittest.TestCase):

    def setUp(self):
        client = GenderAIMLTestClient()
        self._client_context = client.create_client_context("testid")

    def test_gender(self):
        response = self._client_context.bot.ask_question(self._client_context,  "TEST GENDER")
        self.assertIsNotNone(response)
        self.assertEqual(response, "This goes to her.")

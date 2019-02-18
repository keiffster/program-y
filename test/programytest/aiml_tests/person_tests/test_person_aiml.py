import unittest
import os

from programytest.client import TestClient


class PersonTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(PersonTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])
        self.add_person_store(os.path.dirname(__file__)+ os.sep + "person.txt")


class PersonAIMLTests(unittest.TestCase):

    def setUp(self):
        client = PersonTestClient()
        self._client_context = client.create_client_context("testid")

    def test_person(self):
        response = self._client_context.bot.ask_question(self._client_context,  "TEST PERSON")
        self.assertIsNotNone(response)
        self.assertEqual(response, "This is your cat.")

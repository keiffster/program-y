import unittest
import os

from programytest.client import TestClient


class Person2TestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(Person2TestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])
        self.add_person2_store(os.path.dirname(__file__)+ os.sep + "person2.txt")


class Person2AIMLTests(unittest.TestCase):

    def setUp(self):
        client = Person2TestClient()
        self._client_context = client.create_client_context("testid")

    def test_person2(self):
        response = self._client_context.bot.ask_question(self._client_context,  "TEST PERSON2")
        self.assertIsNotNone(response)
        self.assertEqual(response, "He or she was going.")

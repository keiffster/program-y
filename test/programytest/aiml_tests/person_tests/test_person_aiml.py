import unittest
import os

from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient


class PersonTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(PersonTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files = [os.path.dirname(__file__)]
        self.configuration.client_configuration.configurations[0].configurations[0].files._person = os.path.dirname(__file__)+ os.sep + "person.txt"


class PersonAIMLTests(unittest.TestCase):

    def setUp(self):
        client = PersonTestClient()
        self._client_context = client.create_client_context("testid")

    def test_person(self):
        response = self._client_context.bot.ask_question(self._client_context,  "TEST PERSON")
        self.assertIsNotNone(response)
        self.assertEqual(response, "This is your cat")

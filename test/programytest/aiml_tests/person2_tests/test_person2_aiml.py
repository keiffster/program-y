import unittest
import os

from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient


class Person2TestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(Person2TestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files = [os.path.dirname(__file__)]
        self.configuration.client_configuration.configurations[0].configurations[0].files._person2 = os.path.dirname(__file__)+ os.sep + "person2.txt"

class Person2AIMLTests(unittest.TestCase):

    def setUp(self):
        client = Person2TestClient()
        self._client_context = client.create_client_context("testid")

    def test_person2(self):
        response = self._client_context.bot.ask_question(self._client_context,  "TEST PERSON2")
        self.assertIsNotNone(response)
        self.assertEqual(response, "he or she was going")

import unittest
import os

from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient

class GenderAIMLTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(GenderAIMLTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files = [os.path.dirname(__file__)]
        self.configuration.client_configuration.configurations[0].configurations[0].files._gender = os.path.dirname(__file__)+ os.sep + "gender.txt"

class GenderAIMLTests(unittest.TestCase):

    def setUp(self):
        client = GenderAIMLTestClient()
        self._client_context = client.create_client_context("testid")

    def test_gender(self):
        response = self._client_context.bot.ask_question(self._client_context,  "TEST GENDER")
        self.assertIsNotNone(response)
        self.assertEqual(response, "This goes to her")

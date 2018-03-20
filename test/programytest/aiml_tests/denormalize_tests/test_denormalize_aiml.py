import unittest
import os

from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient

class DenormalizeAIMLTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(DenormalizeAIMLTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files = [os.path.dirname(__file__)]
        self.configuration.client_configuration.configurations[0].configurations[0].files._denormal = os.path.dirname(__file__)+ os.sep + "denormal.txt"

class DenormalizeAIMLTests(unittest.TestCase):

    def setUp(self):
        client = DenormalizeAIMLTestClient()
        self._client_context = client.create_client_context("testid")

    def test_denormalize(self):
        response = self._client_context.bot.ask_question(self._client_context,  "TEST DENORMALIZE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "keithsterling.com")

    def test_newdev7_say(self):
        response = self._client_context.bot.ask_question(self._client_context,  "SAY abc dot com")
        self.assertIsNotNone(response)
        self.assertEqual(response, "abc.com")

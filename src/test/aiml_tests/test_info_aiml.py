import unittest
from test.aiml_tests.client import TestClient
from programy.config import BrainFileConfiguration
import logging

class BasicTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(BasicTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration("/Users/keithsterling/Documents/Development/Python/Projects/AIML/program-y/src/test/aiml_tests/test_files/info", ".aiml", False)

class InfoAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        InfoAIMLTests.test_client = BasicTestClient()

    def test_program(self):
        response = InfoAIMLTests.test_client.bot.ask_question("test",  "TEST PROGRAM")
        self.assertIsNotNone(response)
        self.assertEqual(response, "AIMLBot")

    def test_id(self):
        response = InfoAIMLTests.test_client.bot.ask_question("test", "TEST ID")
        self.assertIsNotNone(response)
        self.assertEqual(response, "test")

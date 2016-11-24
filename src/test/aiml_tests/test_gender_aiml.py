import unittest
from test.aiml_tests.client import TestClient
from programy.config import BrainFileConfiguration
import logging

class BasicTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(BasicTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration("/Users/keithsterling/Documents/Development/Python/Projects/AIML/program-y/src/test/aiml_tests/test_files/gender", ".aiml", False)
        self.configuration.brain_configuration._gender = "/Users/keithsterling/Documents/Development/Python/Projects/AIML/program-y/bots/keiffx/config/gender.txt"

class GenderAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        GenderAIMLTests.test_client = BasicTestClient()

    def test_gender(self):
        response = GenderAIMLTests.test_client.bot.ask_question("test",  "TEST GENDER")
        self.assertIsNotNone(response)
        self.assertEqual(response, "This goes to her")

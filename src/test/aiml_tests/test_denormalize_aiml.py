import unittest
from test.aiml_tests.client import TestClient
from programy.config import BrainFileConfiguration
import logging

class BasicTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(BasicTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration("/Users/keithsterling/Documents/Development/Python/Projects/AIML/program-y/src/test/aiml_tests/test_files/denormalize", ".aiml", False)
        self.configuration.brain_configuration._denormal = "/Users/keithsterling/Documents/Development/Python/Projects/AIML/program-y/bots/keiffx/config/denormal.txt"

class DenormalizeAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        DenormalizeAIMLTests.test_client = BasicTestClient()

    def test_denormalize(self):
        response = DenormalizeAIMLTests.test_client.bot.ask_question("test",  "TEST DENORMALIZE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "keithsterling.com")

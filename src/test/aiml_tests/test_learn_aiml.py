import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config import BrainFileConfiguration

class LearnTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(LearnTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration(os.path.dirname(__file__)+"/../aiml_tests/test_files/learn", ".aiml", False)

class LearnAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        LearnAIMLTests.test_client = LearnTestClient()

    def test_learn(self):
        response = LearnAIMLTests.test_client.bot.ask_question("test", "MY NAME IS FRED")
        self.assertIsNotNone(response)
        self.assertEqual(response, "OK, I will remember your name is FRED")

        response = LearnAIMLTests.test_client.bot.ask_question("test", "WHAT IS MY NAME")
        self.assertIsNotNone(response)
        self.assertEqual(response, "YOUR NAME IS FRED")

import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config.brain import BrainFileConfiguration

class LearnfTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(LearnfTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration(os.path.dirname(__file__), ".aiml", False)

class LearnfAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        LearnfAIMLTests.test_client = LearnfTestClient()

    def test_learnf(self):

        LearnfAIMLTests.test_client.bot.brain._configuration._aiml_files = BrainFileConfiguration("/tmp", ".aiml", False)

        response = LearnfAIMLTests.test_client.bot.ask_question("test", "MY NAME IS FRED")
        self.assertIsNotNone(response)
        self.assertEqual(response, "OK, I will remember your name is FRED")

        response = LearnfAIMLTests.test_client.bot.ask_question("test", "WHAT IS MY NAME")
        self.assertIsNotNone(response)
        self.assertEqual(response, "YOUR NAME IS FRED")

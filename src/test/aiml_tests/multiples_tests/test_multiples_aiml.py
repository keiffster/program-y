import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config import BrainFileConfiguration

class MultiplesTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(MultiplesTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration(os.path.dirname(__file__), ".aiml", False)

class MultiplesAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        MultiplesAIMLTests.test_client = MultiplesTestClient()

    def test_multiple_questionsn(self):
        MultiplesAIMLTests.test_client.bot.brain.dump_tree()
        response = MultiplesAIMLTests.test_client.bot.ask_question("test", "HELLO. HOW ARE YOU")
        self.assertIsNotNone(response)
        self.assertEqual("HI THERE. I AM WELL THANKS", response)



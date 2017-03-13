import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config import BrainFileConfiguration

class BasicTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(BasicTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration(os.path.dirname(__file__), ".aiml", False)
        self.configuration.brain_configuration._set_files = BrainFileConfiguration(os.path.dirname(__file__)+"/sets", ".txt", False)

class PatternsetAIMLTests(unittest.TestCase):

    def setUp(cls):
        PatternsetAIMLTests.test_client = BasicTestClient()

    def test_patten_set_match(self):
        response = PatternsetAIMLTests.test_client.bot.ask_question("test",  "MY FAVORITE COLOR IS RED")
        self.assertEqual(response, "RED IS A NICE COLOR.")

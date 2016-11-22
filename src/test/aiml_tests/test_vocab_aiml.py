import unittest
from test.aiml_tests.client import TestClient
from programy.config import BrainFileConfiguration
import logging

class BasicTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(BasicTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration("/Users/keithsterling/Documents/Development/Python/Projects/AIML/program-y/src/test/aiml_tests/test_files/vocab", ".aiml", False)

class VocabularyAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        VocabularyAIMLTests.test_client = BasicTestClient()

    def test_vocabulary(self):
        response = VocabularyAIMLTests.test_client.bot.ask_question("test",  "TEST VOCABULARY")
        self.assertIsNotNone(response)
        self.assertEqual(response, "My vocabulary is 3 words")

    def test_size(self):
        response = VocabularyAIMLTests.test_client.bot.ask_question("test", "TEST SIZE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "I can answer 2 questions")

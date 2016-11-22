import unittest
import logging

from test.aiml_tests.client import TestClient
from programy.config import BrainFileConfiguration

class TopicStarTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(TopicStarTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration("/Users/keithsterling/Documents/Development/Python/Projects/AIML/program-y/src/test/aiml_tests/test_files/topicstar", ".aiml", False)

class TopicStarAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        TopicStarAIMLTests.test_client = TopicStarTestClient()

    def test_single_topicstar_word(self):

        response = TopicStarAIMLTests.test_client.bot.ask_question("test", "HELLO")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HELLO STAR TOPIC')


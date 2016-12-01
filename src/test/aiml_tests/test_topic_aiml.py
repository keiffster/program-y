import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config import BrainFileConfiguration

class TopicTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(TopicTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration(os.path.dirname(__file__)+"/../aiml_tests/test_files/topic", ".aiml", False)

class TopicAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        TopicAIMLTests.test_client = TopicTestClient()

    def test_topic_single_topic_word(self):

        response = TopicAIMLTests.test_client.bot.ask_question("test", "HI THERE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'OUTSIDE OF TEST1TOPIC')

        response = TopicAIMLTests.test_client.bot.ask_question("test", "HELLO")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'INSIDE OF TEST1TOPIC')

    def test_topic_multiple_topic_words(self):
        response = TopicAIMLTests.test_client.bot.ask_question("test", "SEEYA")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'OUTSIDE OF TEST2 TOPIC')

        response = TopicAIMLTests.test_client.bot.ask_question("test", "GOODBYE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'INSIDE OF TEST2 TOPIC')

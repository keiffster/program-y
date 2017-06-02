import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config.brain import BrainFileConfiguration

# TODO <that><topic> can take single "1" and double "1,2" indexes

class TopicTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(TopicTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration(files=os.path.dirname(__file__))

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

    def test_topic_wildcard_topic_words(self):
        response = TopicAIMLTests.test_client.bot.ask_question("test", "WILDCARD1")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'WILDCARD1 TEST OK')

        response = TopicAIMLTests.test_client.bot.ask_question("test", "WILDCARD2")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'WILDCARD2 TEST OK')

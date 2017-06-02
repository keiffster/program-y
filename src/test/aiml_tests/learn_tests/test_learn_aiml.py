import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config.brain import BrainFileConfiguration

class LearnTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(LearnTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration(files=os.path.dirname(__file__))

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

    def test_learn_x_is_y(self):

        response = LearnAIMLTests.test_client.bot.ask_question("test", "LEARN THE SUN IS HOT")
        self.assertIsNotNone(response)
        self.assertEqual(response, "OK, I will remember THE SUN is HOT")

        response = LearnAIMLTests.test_client.bot.ask_question("test", "LEARN THE SKY IS BLUE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "OK, I will remember THE SKY is BLUE")

        response = LearnAIMLTests.test_client.bot.ask_question("test", "LEARN THE MOON IS GREY")
        self.assertIsNotNone(response)
        self.assertEqual(response, "OK, I will remember THE MOON is GREY")

        LearnAIMLTests.test_client.bot.brain.dump_tree()

        response = LearnAIMLTests.test_client.bot.ask_question("test", "WHAT IS THE SUN")
        self.assertIsNotNone(response)
        self.assertEqual(response, "HOT")

        response = LearnAIMLTests.test_client.bot.ask_question("test", "WHAT IS THE SKY")
        self.assertIsNotNone(response)
        self.assertEqual(response, "BLUE")

        response = LearnAIMLTests.test_client.bot.ask_question("test", "WHAT IS THE MOON")
        self.assertIsNotNone(response)
        self.assertEqual(response, "GREY")

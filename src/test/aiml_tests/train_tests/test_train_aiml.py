import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config.file.factory import ConfigurationFactory
from programy.config.client.client import ClientConfiguration

class TrainTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        self.configuration = ClientConfiguration()
        ConfigurationFactory.load_configuration_from_file(self.configuration, os.path.dirname(__file__)+"/testconfig.yaml")

class TrainAIMLTests(unittest.TestCase):

    def setUp(cls):
        TrainAIMLTests.test_client = TrainTestClient()

    def test_train_noun(self):

        TrainAIMLTests.test_client.bot.brain.dump_tree()

        response = TrainAIMLTests.test_client.bot.ask_question("test", "jessica likes to smoke cigars")
        self.assertIsNotNone(response)
        self.assertEqual("Do you smoke cigars too?", response)

        response = TrainAIMLTests.test_client.bot.ask_question("test", "who likes to smoke cigars")
        self.assertIsNotNone(response)
        self.assertEqual("Jessica likes to smoke cigars", response)

        response = TrainAIMLTests.test_client.bot.ask_question("test", "who likes to smoke cigars")
        self.assertIsNotNone(response)
        self.assertEqual("Jessica likes to smoke cigars", response)

        response = TrainAIMLTests.test_client.bot.ask_question("test", "what does jessica like")
        self.assertIsNotNone(response)
        self.assertEqual("Jessica likes to smoke cigars", response)

        response = TrainAIMLTests.test_client.bot.ask_question("test", "what does jessica smoke")
        self.assertIsNotNone(response)
        self.assertEqual("Jessica likes to smoke cigars", response)

        response = TrainAIMLTests.test_client.bot.ask_question("test", "who smokes")
        self.assertIsNotNone(response)
        self.assertEqual("Jessica likes to smoke cigars", response)

    def test_train_pronoun(self):

        TrainAIMLTests.test_client.bot.brain.dump_tree()

        response = TrainAIMLTests.test_client.bot.ask_question("test", "mommy likes to smoke cigars")
        self.assertIsNotNone(response)

        self.assertEqual('Now you can ask me: "Who likes TO SMOKE CIGARS?" and "What does my mommy like?"', response)

        response = TrainAIMLTests.test_client.bot.ask_question("test", "who likes to smoke cigars")
        self.assertIsNotNone(response)
        self.assertEqual("Your mommy", response)


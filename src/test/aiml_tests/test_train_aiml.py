import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config import ConfigurationFactory

class TrainTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self, debug=True)

    def load_configuration(self, arguments):
        self.configuration = ConfigurationFactory.load_configuration_from_file(os.path.dirname(__file__)+"/test_files/train/testconfig.yaml", "yaml")

class TrainAIMLTests(unittest.TestCase):

    def setUp(cls):
        TrainAIMLTests.test_client = TrainTestClient()

    def test_train_noun(self):
        TrainAIMLTests.test_client.bot.brain.dump_tree()
        response = TrainAIMLTests.test_client.bot.ask_question("test", "JESSICA LIKES TO SMOKE CIGARS")
        self.assertIsNotNone(response)
        self.assertEqual("Do you smoke cigars too?", response)

        TrainAIMLTests.test_client.bot.brain.dump_tree()
        response = TrainAIMLTests.test_client.bot.ask_question("test", "WHO LIKES TO SMOKE CIGARS")
        self.assertIsNotNone(response)
        self.assertEqual("Jessica likes to smoke cigars", response)

    def test_train_pronoun(self):
        TrainAIMLTests.test_client.bot.brain.dump_tree()
        response = TrainAIMLTests.test_client.bot.ask_question("test", "MOMMY LIKES TO SMOKE CIGARS")
        self.assertIsNotNone(response)
        self.assertEqual("Do you smoke cigars too?", response)

        TrainAIMLTests.test_client.bot.brain.dump_tree()
        response = TrainAIMLTests.test_client.bot.ask_question("test", "WHO LIKES TO SMOKE CIGARS")
        self.assertIsNotNone(response)
        self.assertEqual("Mommy likes to smoke cigars", response)
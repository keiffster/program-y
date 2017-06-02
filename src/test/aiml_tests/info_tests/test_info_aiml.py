import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config.brain import BrainFileConfiguration

class BasicTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(BasicTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration(files=os.path.dirname(__file__))

class InfoAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        InfoAIMLTests.test_client = BasicTestClient()

    def test_program(self):
        response = InfoAIMLTests.test_client.bot.ask_question("test",  "TEST PROGRAM")
        self.assertIsNotNone(response)
        self.assertEqual(response, "AIMLBot")

    def test_id(self):
        response = InfoAIMLTests.test_client.bot.ask_question("test", "TEST ID")
        self.assertIsNotNone(response)
        self.assertEqual(response, "test")

    def test_env(self):

        InfoAIMLTests.test_client.bot.brain.predicates.pairs.append(["env","test"])

        response = InfoAIMLTests.test_client.bot.ask_question("test", "TEST ENVIRONMENT")
        self.assertIsNotNone(response)
        self.assertEqual(response, "ENVIRONMET IS test")

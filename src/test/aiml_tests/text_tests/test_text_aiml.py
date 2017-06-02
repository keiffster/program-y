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

class TextAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        TextAIMLTests.test_client = BasicTestClient()

    def test_lowercase(self):
        response = TextAIMLTests.test_client.bot.ask_question("test",  "MAKE LOWERCASE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "hello world")

    def test_uppercase(self):
        response = TextAIMLTests.test_client.bot.ask_question("test", "MAKE UPPERCASE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "HELLO WORLD")


    def test_sentence(self):
        response = TextAIMLTests.test_client.bot.ask_question("test", "MAKE SENTENCE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Hello world")


    def test_formal(self):
        response = TextAIMLTests.test_client.bot.ask_question("test", "MAKE FORMAL")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Hello World")


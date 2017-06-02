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

class XPlodeAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        XPlodeAIMLTests.test_client = BasicTestClient()

    def test_explode(self):
        response = XPlodeAIMLTests.test_client.bot.ask_question("test",  "MAKE EXPLODE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "h e l l o w o r l d")

    def test_implode(self):
        response = XPlodeAIMLTests.test_client.bot.ask_question("test", "MAKE IMPLODE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "helloworld")

    def test_nested_explode_implode(self):
        response = XPlodeAIMLTests.test_client.bot.ask_question("test", "NESTED EXPLODE IMPLODE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "helloworld")

    def test_nested_implode_explode(self):
        response = XPlodeAIMLTests.test_client.bot.ask_question("test", "NESTED IMPLODE EXPLODE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "h e l l o w o r l d")

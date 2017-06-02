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

class ThinkAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ThinkAIMLTests.test_client = BasicTestClient()

    def test_think(self):
        response = ThinkAIMLTests.test_client.bot.ask_question("test",  "THINK")
        self.assertIsNotNone(response)
        self.assertEqual(response, "")

    def test_set_think(self):
        response = ThinkAIMLTests.test_client.bot.ask_question("test", "SET THINK")
        self.assertIsNotNone(response)
        self.assertEqual(response, "")

        self.assertEquals("Keith", ThinkAIMLTests.test_client.bot.get_conversation("test").current_question().predicate("name"))

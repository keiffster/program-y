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

class PatternBotAIMLTests(unittest.TestCase):

    def setUp(cls):
        PatternBotAIMLTests.test_client = BasicTestClient()
        PatternBotAIMLTests.test_client.bot.brain.properties.pairs.append(("favouritecolor", "RED"))

    def test_pattern_bot_match(self):
        PatternBotAIMLTests.test_client.bot.brain.dump_tree()

        response = PatternBotAIMLTests.test_client.bot.ask_question("test",  "MY FAVORITE COLOR IS RED")
        self.assertIsNotNone(response)
        self.assertEqual(response, "RED IS A NICE COLOR.")


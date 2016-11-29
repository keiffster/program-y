import unittest
from test.aiml_tests.client import TestClient
from programy.config import BrainFileConfiguration
import logging

class BasicTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(BasicTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration("/Users/keithsterling/Documents/Development/Python/Projects/AIML/program-y/src/test/aiml_tests/test_files/map", ".aiml", False)

class MapAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        MapAIMLTests.test_client = BasicTestClient()
        MapAIMLTests.test_client.bot.brain.maps._maps["MAP1"] = { "MAPVAL1": "VAL1", "MAPVAL2": "VAL2", "MAPVAL3": "VAL3" }

    def test_name_map_topic(self):
        response = MapAIMLTests.test_client.bot.ask_question("test",  "NAME MAP")
        self.assertIsNotNone(response)
        self.assertEqual(response, "OK VAL1")

    def test_multi_word_name_map_topic(self):
        response = MapAIMLTests.test_client.bot.ask_question("test",  "MULTI WORD NAME MAP")
        self.assertIsNotNone(response)
        self.assertEqual(response, "OK VAL1")

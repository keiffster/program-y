import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config.sections.brain.file import BrainFileConfiguration

class BasicTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(BasicTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration.files.aiml_files._files = os.path.dirname(__file__)

class MapAIMLTests(unittest.TestCase):

    def setUp(self):
        MapAIMLTests.test_client = BasicTestClient()
        MapAIMLTests.test_client.bot.brain.properties.load_from_text("""
             default-get:unknown
         """)
        MapAIMLTests.test_client.bot.brain.configuration.dynamics.add_dynamic_map('romantodec', "programy.dynamic.maps.roman.MapRomanToDecimal", None)
        MapAIMLTests.test_client.bot.brain.configuration.dynamics.add_dynamic_map('dectoroman', "programy.dynamic.maps.roman.MapDecimalToRoman", None)

    def test_dynamic_map(self):
        response = MapAIMLTests.test_client.bot.ask_question("test",  "DYNAMIC MAP DECIMAL TO ROMAN")
        self.assertEqual(response, "20 is XX")

        response = MapAIMLTests.test_client.bot.ask_question("test",  "DYNAMIC MAP ROMAN TO DECIMAL")
        self.assertEqual(response, "XX is 20")

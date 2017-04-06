import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config.brain import BrainFileConfiguration


class MapsTestsClient(TestClient):

    def __init__(self):
        TestClient.__init__(self, debug=True)

    def load_configuration(self, arguments):
        super(MapsTestsClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration(os.path.dirname(__file__)+"/../../../../aiml/extensions/maps", ".aiml", False)

class MapsAIMLTests(unittest.TestCase):

    def setUp (self):
        MapsAIMLTests.test_client = MapsTestsClient()

    def test_distance(self):
        response = MapsAIMLTests.test_client.bot.ask_question("testif", "DISTANCE EDINBURGH KINGHORN")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'DISTANCE DEC 25 FRAC 5 UNITS mi')

    def test_directions(self):
        response = MapsAIMLTests.test_client.bot.ask_question("testif", "DIRECTIONS EDINBURGH KINGHORN")
        self.assertIsNotNone(response)
        self.assertTrue(response.startswith("DIRECTIONS Head west on Leith St/A900"))

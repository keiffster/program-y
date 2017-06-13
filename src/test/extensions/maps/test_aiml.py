import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config.brain import BrainFileConfiguration


class MapsTestsClient(TestClient):

    def __init__(self):
        TestClient.__init__(self, debug=True)

    def load_configuration(self, arguments):
        super(MapsTestsClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration(files=os.path.dirname(__file__))

class MapsAIMLTests(unittest.TestCase):

    def setUp (self):
        MapsAIMLTests.test_client = MapsTestsClient()

        latlong     = os.path.dirname(__file__) + "/google_latlong.json"
        distance    = os.path.dirname(__file__) + "/distance.json"
        directions  = os.path.dirname(__file__) + "/directions.json"

        MapsAIMLTests.test_client.bot.license_keys.load_license_key_data("""
        GOOGLE_LATLONG=%s
        GOOGLE_MAPS_DISTANCE=%s
        GOOGLE_MAPS_DIRECTIONS=%s
        """%(latlong, distance, directions))

    def test_distance(self):
        response = MapsAIMLTests.test_client.bot.ask_question("testif", "DISTANCE EDINBURGH KINGHORN")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'It is 25 . 1 miles')

    def test_directions(self):
        response = MapsAIMLTests.test_client.bot.ask_question("testif", "DIRECTIONS EDINBURGH KINGHORN")
        self.assertIsNotNone(response)
        self.assertTrue(response.startswith("To get there Head west on Leith St"))

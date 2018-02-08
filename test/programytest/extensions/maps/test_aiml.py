import unittest
import os
import json

from programy.extensions.maps.maps import GoogleMapsExtension
from programy.utils.geo.google import GoogleMaps
from programytest.aiml_tests.client import TestClient

class MockGoogleMaps(GoogleMaps):

    def __init__(self, response_file):
        self._response_file = response_file

    def _get_response_as_json(self, url):
        with open(self._response_file) as response_data:
            return json.load(response_data)


class MockGoogleMapsExtension(GoogleMapsExtension):

    response_file = None

    def get_geo_locator(self):
        return MockGoogleMaps(MockGoogleMapsExtension.response_file)

class MapsTestsClient(TestClient):

    def __init__(self):
        TestClient.__init__(self, debug=True)

    def load_configuration(self, arguments):
        super(MapsTestsClient, self).load_configuration(arguments)
        self.configuration.brain_configuration.files.aiml_files._files=[os.path.dirname(__file__)]


class MapsAIMLTests(unittest.TestCase):

    def setUp (self):
        MapsAIMLTests.test_client = MapsTestsClient()

    def test_distance(self):
        MockGoogleMapsExtension.response_file    = os.path.dirname(__file__) +  os.sep + "distance.json"

        response = MapsAIMLTests.test_client.bot.ask_question("testif", "DISTANCE EDINBURGH KINGHORN")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'It is 25 . 1 miles')

    def test_directions(self):
        MockGoogleMapsExtension.response_file    = os.path.dirname(__file__) +  os.sep + "directions.json"

        response = MapsAIMLTests.test_client.bot.ask_question("testif", "DIRECTIONS EDINBURGH KINGHORN")
        self.assertIsNotNone(response)
        self.assertTrue(response.startswith("To get there Head west on Leith St"))

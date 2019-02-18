import unittest
import unittest.mock
import os
import json

from programy.extensions.maps.maps import GoogleMapsExtension
from programy.utils.geo.google import GoogleDistance
from programy.utils.geo.google import GoogleMaps

from programytest.client import TestClient

class MockGoogleMaps(GoogleMaps):

    def __init__(self, response_file):
        self._response_file = response_file

    def _get_response_as_json(self, url):
        with open(self._response_file) as response_data:
            return json.load(response_data)


class MockGoogleMapsExtension(GoogleMapsExtension):

    def __init__(self, response_file):
        self._response_file = response_file

    def get_geo_locator(self):
        return MockGoogleMaps(self._response_file)


class MapsExtensionTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        self.context = client.create_client_context("testid")

    def test_maps_distance(self):
        distance    = os.path.dirname(__file__) +  os.sep + "distance.json"

        googlemaps = MockGoogleMapsExtension(distance)
        self.assertIsNotNone(googlemaps)

        result = googlemaps.execute(self.context, "DISTANCE EDINBURGH KINGHORN")
        self.assertIsNotNone(result)
        self.assertEqual("DISTANCE DEC 25 FRAC 1 UNITS miles", result)

    def test_maps_direction(self):
        directions  = os.path.dirname(__file__) +  os.sep + "directions.json"

        googlemaps = MockGoogleMapsExtension(directions)
        self.assertIsNotNone(googlemaps)

        result = googlemaps.execute(self.context, "DIRECTIONS EDINBURGH KINGHORN")
        self.assertIsNotNone(result)
        self.assertTrue(result.startswith("DIRECTIONS Head west on Leith St/A900 toward Leith"))

    def test_maps_unknown(self):
        latlong     = os.path.dirname(__file__) +  os.sep + "google_latlong.json"

        googlemaps = MockGoogleMapsExtension(latlong)
        self.assertIsNotNone(googlemaps)

        result = googlemaps.execute(self.context, "SOMETHINGELSE EDINBURGH KINGHORN")
        self.assertIsNone(result)

    def test_format_distance_for_programy(self):
        distance    = os.path.dirname(__file__) +  os.sep + "distance.json"

        googlemaps = MockGoogleMapsExtension(distance)
        self.assertIsNotNone(googlemaps)

        distance = GoogleDistance("here", "there")
        distance._distance_text = "10 miles"
        self.assertEqual("DISTANCE DEC 10 FRAC 0 UNITS miles", googlemaps._format_distance_for_programy(distance))

        distance = GoogleDistance("here", "there")
        distance._distance_text = "22.45 km"
        self.assertEqual("DISTANCE DEC 22 FRAC 45 UNITS km", googlemaps._format_distance_for_programy(distance))

    def test_format_directions_for_programy(self):
        directions  = os.path.dirname(__file__) +  os.sep + "directions.json"

        googlemaps = MockGoogleMapsExtension(directions)
        self.assertIsNotNone(googlemaps)

        directions = unittest.mock.Mock()
        directions.legs_as_a_string = lambda : "Leg As String"
        self.assertEqual("DIRECTIONS Leg As String", googlemaps._format_directions_for_programy(directions))

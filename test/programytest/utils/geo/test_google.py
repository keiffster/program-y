import unittest
import os
import json

from programy.utils.geo.google import GoogleMaps, GoogleDistance, GoogleDirections
from programy.utils.geo.latlong import LatLong

#############################################################################
#

class MockGoogleMaps(GoogleMaps):

    def __init__(self, data_file_name):
        self._data_file_name = data_file_name

    def _get_response_as_json(self, url):
        with open(self._data_file_name, "r") as data_file:
            return json.load(data_file)


class GoogleMapsTests(unittest.TestCase):

    def test_location(self):
        filename = os.path.dirname(__file__) + os.sep + "google_latlong.json"
        self.assertTrue(os.path.isfile(filename))
        googlemaps = MockGoogleMaps(filename)
        self.assertIsNotNone(googlemaps)

        latlng = googlemaps.get_latlong_for_location("KY3 9UR")
        self.assertIsNotNone(latlng)
        self.assertIsInstance(latlng, LatLong)
        self.assertEqual(latlng.latitude, 56.0720397)
        self.assertEqual(latlng.longitude, -3.1752001)

    def test_distance_uk_driving_imperial(self):
        filename = os.path.dirname(__file__) + os.sep + "distance.json"
        self.assertTrue(os.path.isfile(filename))
        googlemaps = MockGoogleMaps(filename)
        self.assertIsNotNone(googlemaps)

        distance = googlemaps.get_distance_between_addresses("Edinburgh", "London", country="UK", mode="driving", units="imperial")
        self.assertIsNotNone(distance)
        self.assertIsInstance(distance, GoogleDistance)
        self.assertEqual("25.1 mi", distance._distance_text)

    def test_directions(self):
        filename = os.path.dirname(__file__) + os.sep + "directions.json"
        self.assertTrue(os.path.isfile(filename))
        googlemaps = MockGoogleMaps(filename)
        self.assertIsNotNone(googlemaps)

        directions = googlemaps.get_directions_between_addresses("Edinburgh", "London")
        self.assertIsNotNone(directions)
        self.assertIsInstance(directions, GoogleDirections)


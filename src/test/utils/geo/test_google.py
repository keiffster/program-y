import unittest
import os

from programy.utils.geo.google import GoogleMaps, GoogleDistance, GoogleDirections
from programy.utils.geo.latlong import LatLong

#############################################################################
#

class GoogleMapsTests(unittest.TestCase):

    def test_location(self):
        googlemaps = GoogleMaps(None)

        filename = os.path.dirname(__file__) + "/google_latlong.json"
        # If this line fails, you need to generate test data using programy.utils.geo.google_geo.GoogleMaps static methods
        self.assertTrue(os.path.isfile(filename))

        googlemaps.set_response_file_for_get_latlong_for_location(filename)

        latlng = googlemaps.get_latlong_for_location("KY3 9UR")
        self.assertIsNotNone(latlng)
        self.assertIsInstance(latlng, LatLong)
        self.assertEquals(latlng.latitude, 56.0720397)
        self.assertEquals(latlng.longitude, -3.1752001)

    def test_distance_uk_driving_imperial(self):
        googlemaps = GoogleMaps(None)

        filename = os.path.dirname(__file__) + "/distance.json"
        # If this line fails, you need to generate test data using programy.utils.geo.google_geo.GoogleMaps static methods
        self.assertTrue(os.path.isfile(filename))

        googlemaps.set_response_file_for_get_distance_between_addresses(filename)

        distance = googlemaps.get_distance_between_addresses("Edinburgh", "London", country="UK", mode="driving", units="imperial")
        self.assertIsNotNone(distance)
        self.assertIsInstance(distance, GoogleDistance)
        self.assertEquals("25.1 mi", distance._distance_text)

    def test_directions(self):
        googlemaps = GoogleMaps(None)

        filename = os.path.dirname(__file__) + "/directions.json"
        # If this line fails, you need to generate test data using programy.utils.geo.google_geo.GoogleMaps static methods
        self.assertTrue(os.path.isfile(filename))

        googlemaps.set_response_file_for_get_directions_between_addresses(filename)

        directions = googlemaps.get_directions_between_addresses("Edinburgh", "London")
        self.assertIsNotNone(directions)
        self.assertIsInstance(directions, GoogleDirections)


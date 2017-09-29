import unittest
import unittest.mock

from programy.extensions.maps.maps import GoogleMapsExtension
from programy.utils.geo.google import GoogleDistance
from programytest.aiml_tests.client import TestClient
import os

class MapsExtensionTests(unittest.TestCase):

    def setUp(self):
        self.test_client = TestClient()

        latlong     = os.path.dirname(__file__) +  os.sep + "google_latlong.json"
        distance    = os.path.dirname(__file__) +  os.sep + "distance.json"
        directions  = os.path.dirname(__file__) +  os.sep + "directions.json"

        self.test_client.bot.license_keys.load_license_key_data("""
        GOOGLE_LATLONG=%s
        GOOGLE_MAPS_DISTANCE=%s
        GOOGLE_MAPS_DIRECTIONS=%s
        """%(latlong, distance, directions))

    def test_maps_distance(self):
        googlemaps = GoogleMapsExtension()
        self.assertIsNotNone(googlemaps)

        result = googlemaps.execute(self.test_client.bot, "testid", "DISTANCE EDINBURGH KINGHORN")
        self.assertIsNotNone(result)
        self.assertEquals("DISTANCE DEC 25 FRAC 1 UNITS miles", result)

    def test_maps_direction(self):
        googlemaps = GoogleMapsExtension()
        self.assertIsNotNone(googlemaps)

        result = googlemaps.execute(self.test_client.bot, "testid", "DIRECTIONS EDINBURGH KINGHORN")
        self.assertIsNotNone(result)
        self.assertTrue(result.startswith("DIRECTIONS Head west on Leith St/A900 toward Leith"))

    def test_maps_unknown(self):
        googlemaps = GoogleMapsExtension()
        self.assertIsNotNone(googlemaps)

        result = googlemaps.execute(self.test_client.bot, "testid", "SOMETHINGELSE EDINBURGH KINGHORN")
        self.assertIsNone(result)

    def test_format_distance_for_programy(self):
        googlemaps = GoogleMapsExtension()
        self.assertIsNotNone(googlemaps)

        distance = GoogleDistance("here", "there")
        distance._distance_text = "10 miles"
        self.assertEquals("DISTANCE DEC 10 FRAC 0 UNITS miles", googlemaps._format_distance_for_programy(distance))

        distance = GoogleDistance("here", "there")
        distance._distance_text = "22.45 km"
        self.assertEquals("DISTANCE DEC 22 FRAC 45 UNITS km", googlemaps._format_distance_for_programy(distance))

    def test_format_directions_for_programy(self):
        googlemaps = GoogleMapsExtension()
        self.assertIsNotNone(googlemaps)

        directions = unittest.mock.Mock()
        directions.legs_as_a_string = lambda : "Leg As String"
        self.assertEquals("DIRECTIONS Leg As String", googlemaps._format_directions_for_programy(directions))

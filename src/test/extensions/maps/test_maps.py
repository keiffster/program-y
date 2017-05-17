import unittest

from programy.extensions.maps.maps import GoogleMapsExtension
from test.aiml_tests.client import TestClient
import os

class MapsExtensionTests(unittest.TestCase):

    def setUp(self):
        self.test_client = TestClient()

        latlong     = os.path.dirname(__file__) + "/google_latlong.json"
        distance    = os.path.dirname(__file__) + "/distance.json"
        directions  = os.path.dirname(__file__) + "/directions.json"

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

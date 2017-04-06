import unittest

from extensions.maps.maps import GoogleMapsExtension
from test.aiml_tests.client import TestClient

#TODO Mock out responses, these tests currently call live Google maps API

class MapsExtensionTests(unittest.TestCase):

    def setUp(self):
        self.test_client = TestClient()

    def test_maps_distance(self):
        googlemaps = GoogleMapsExtension()
        self.assertIsNotNone(googlemaps)

        result = googlemaps.execute(self.test_client.bot, "testid", "DISTANCE EDINBURGH KINGHORN")
        self.assertIsNotNone(result)
        self.assertEquals("DISTANCE DEC 25 FRAC 5 UNITS mi", result)

    def test_maps_direction(self):
        googlemaps = GoogleMapsExtension()
        self.assertIsNotNone(googlemaps)

        result = googlemaps.execute(self.test_client.bot, "testid", "DIRECTIONS EDINBURGH KINGHORN")
        self.assertIsNotNone(result)
        self.assertTrue(result.startswith("DIRECTIONS Head west on Leith St/A900 toward Leith"))

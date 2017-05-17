import unittest

from programy.extensions.geocode.geocode import GeoCodeExtension
from test.aiml_tests.client import TestClient
import os

class GeoCodeExtensionTests(unittest.TestCase):

    def setUp(self):
        self.test_client = TestClient()

        latlong     = os.path.dirname(__file__) + "/google_latlong.json"

        self.test_client.bot.license_keys.load_license_key_data("""
        GOOGLE_LATLONG = %s
        """%(latlong))

    def test_geocode_postcode1(self):
        geocode = GeoCodeExtension()
        self.assertIsNotNone(geocode)

        result = geocode.execute(self.test_client.bot, "testid", "POSTCODE1 KY39UR")
        self.assertIsNotNone(result)
        self.assertEquals("LATITUDE DEC 56 FRAC 0720397 LONGITUDE DEC -3 FRAC 1752001", result)

    def test_geocode_postcode2(self):
        geocode = GeoCodeExtension()
        self.assertIsNotNone(geocode)

        result = geocode.execute(self.test_client.bot, "testid", "POSTCODE2 KY3 9UR")
        self.assertIsNotNone(result)
        self.assertEquals("LATITUDE DEC 56 FRAC 0720397 LONGITUDE DEC -3 FRAC 1752001", result)

    def test_geocode_location(self):
        geocode = GeoCodeExtension()
        self.assertIsNotNone(geocode)

        result = geocode.execute(self.test_client.bot, "testid", "LOCATION KINGHORN")
        self.assertIsNotNone(result)
        self.assertEquals("LATITUDE DEC 56 FRAC 0720397 LONGITUDE DEC -3 FRAC 1752001", result)
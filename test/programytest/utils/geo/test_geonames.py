import unittest
import os

from programy.utils.geo.geonames import GeoNamesApi
from programy.utils.license.keys import LicenseKeys
from programytest.client import TestClient

#############################################################################
#

class GeoNamesTests(unittest.TestCase):

    def test_geonames_no_license_keys(self):
        license_keys = LicenseKeys()
        with self.assertRaises(Exception):
            geonames = GeoNamesApi(license_keys)

    def test_geonames_no_account_name(self):
        license_keys = LicenseKeys()
        license_keys.add_key('GEO_NAMES_COUNTRY', "DummyValue")
        with self.assertRaises(Exception):
            geonames = GeoNamesApi(license_keys)

    def test_geonames_no_country(self):
        license_keys = LicenseKeys()
        license_keys.add_key('GEO_NAMES_ACCOUNTNAME', "DummyValue")
        with self.assertRaises(Exception):
            geonames = GeoNamesApi(license_keys)

    def test_geonames(self):
        client = TestClient()
        client.add_license_keys_store()

        geonames = GeoNamesApi()
        self.assertIsNotNone(geonames)

        GeoNamesApi.get_latlong_for_postcode_response_file = os.path.dirname(__file__)+ os.sep + "geonames_latlong.json"

        latlng = geonames.get_latlong_for_postcode('KY39UR')
        self.assertIsNotNone(latlng)
        self.assertEqual(latlng.latitude, 56.07206267570594)
        self.assertEqual(latlng.longitude, -3.175233048730664)

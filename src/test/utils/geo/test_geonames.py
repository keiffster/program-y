import unittest
import os

from programy.utils.geo.geonames import GeoNamesApi
from programy.utils.license.keys import LicenseKeys

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

    def test_geonames_with_license_keys(self):
        license_keys = LicenseKeys()
        license_keys.add_key('GEO_NAMES_COUNTRY', "DummyValue")
        license_keys.add_key('GEO_NAMES_ACCOUNTNAME', "DummyValue")
        geonames = GeoNamesApi(license_keys)

    def test_geonames(self):

        license_keys = LicenseKeys()
        license_keys.load_license_key_file(os.path.dirname(__file__)+ os.sep + "test.keys")

        geonames = GeoNamesApi(license_keys)
        self.assertIsNotNone(geonames)

        GeoNamesApi.get_latlong_for_postcode_response_file = os.path.dirname(__file__)+ os.sep + "geonames_latlong.json"

        latlng = geonames.get_latlong_for_postcode('KY39UR')
        self.assertIsNotNone(latlng)
        self.assertEquals(latlng.latitude, 56.07206267570594)
        self.assertEquals(latlng.longitude, -3.175233048730664)

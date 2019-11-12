import unittest

from programy.utils.geo.geonames import GeoNamesApi
from programy.utils.license.keys import LicenseKeys
from programytest.client import TestClient


class MockGeoNamesApi(GeoNamesApi):

    def __init__(self, response):
        GeoNamesApi.__init__(self)
        self._response = response

    def _get_latlong_for_postcode_response(self, postcode):
        return self._response


class GeoNamesLatLngTests(unittest.TestCase):

    def test_geonames_license_keys(self):
        license_keys = LicenseKeys()
        license_keys.add_key('GEO_NAMES_COUNTRY', "UK")
        license_keys.add_key('GEO_NAMES_ACCOUNTNAME', "TestAccount1")
        geonames = GeoNamesApi()
        geonames.check_for_license_keys(license_keys)

        self.assertEqual("UK", geonames.country)
        self.assertEqual("TestAccount1", geonames.account_name)

    def test_geonames_missing_license_keys(self):
        license_keys = LicenseKeys()
        geonames = GeoNamesApi()
        with self.assertRaises(Exception):
            geonames.check_for_license_keys(license_keys)

    def test_geonames_no_account_name(self):
        license_keys = LicenseKeys()
        license_keys.add_key('GEO_NAMES_COUNTRY', "DummyValue")
        geonames = GeoNamesApi()
        with self.assertRaises(Exception):
            geonames.check_for_license_keys(license_keys)

    def test_geonames_no_country(self):
        license_keys = LicenseKeys()
        license_keys.add_key('GEO_NAMES_ACCOUNTNAME', "DummyValue")
        geonames = GeoNamesApi()
        with self.assertRaises(Exception):
            geonames.check_for_license_keys(license_keys)

    def test_geonames(self):
        client = TestClient()
        client.add_license_keys_store()

        geonames = MockGeoNamesApi(response={ "postalCodes": [
                                                {
                                                  "lat": 56.07206267570594,
                                                  "lng": -3.175233048730664
                                                }
                                              ]
                                            })
        self.assertIsNotNone(geonames)

        latlng = geonames.get_latlong_for_postcode('KY39UR')
        self.assertIsNotNone(latlng)
        self.assertEqual(latlng.latitude, 56.07206267570594)
        self.assertEqual(latlng.longitude, -3.175233048730664)

    def test_geonames_no_postcodes(self):
        client = TestClient()
        client.add_license_keys_store()

        geonames = MockGeoNamesApi(response={})
        self.assertIsNotNone(geonames)

        with self.assertRaises(Exception):
            _ = geonames.get_latlong_for_postcode('KY39UR')

    def test_geonames_empty_postcodes(self):
        client = TestClient()
        client.add_license_keys_store()

        geonames = MockGeoNamesApi(response={
                                              "postalCodes": []
                                            })
        self.assertIsNotNone(geonames)

        with self.assertRaises(Exception):
            _ = geonames.get_latlong_for_postcode('KY39UR')

    def test_geonames_no_lat_long(self):
        client = TestClient()
        client.add_license_keys_store()

        geonames = MockGeoNamesApi(response={
                                              "postalCodes": [
                                                {
                                                }
                                              ]
                                            })
        self.assertIsNotNone(geonames)

        with self.assertRaises(Exception):
            _ = geonames.get_latlong_for_postcode('KY39UR')

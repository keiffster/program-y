import unittest
import os

from programy.utils.geo.geonames import GeoNamesApi
from programy.utils.license.keys import LicenseKeys

#############################################################################
#

class GeoNamesTests(unittest.TestCase):

    def test_geonames(self):

        license_keys = LicenseKeys()
        license_keys.load_license_key_file(os.path.dirname(__file__)+"/test.keys")

        geonames = GeoNamesApi(license_keys)
        self.assertIsNotNone(geonames)

        GeoNamesApi.get_latlong_for_postcode_response_file = os.path.dirname(__file__)+"/geonames_latlong.json"

        latlng = geonames.get_latlong_for_postcode('KY39UR')
        self.assertIsNotNone(latlng)
        self.assertEquals(latlng.latitude, 56.07206267570594)
        self.assertEquals(latlng.longitude, -3.175233048730664)

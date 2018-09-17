import unittest
import os

from programy.utils.geo.geonames import GeoNamesApi
from programy.utils.license.keys import LicenseKeys

#############################################################################
#

class GeoNamesTests(unittest.TestCase):

    def setUp(self):
        self.license_keys = LicenseKeys()
        self.license_keys.load_license_key_file(os.path.dirname(__file__) + "/../../../../bots/y-bot/config/license.keys")

    def test_geonames(self):

        geonames = GeoNamesApi(self.license_keys)
        self.assertIsNotNone(geonames)

        latlng = geonames.get_latlong_for_postcode('KY39UR')
        self.assertIsNotNone(latlng)
        self.assertEqual(latlng.latitude, 56.07206267570594)
        self.assertEqual(latlng.longitude, -3.175233048730664)

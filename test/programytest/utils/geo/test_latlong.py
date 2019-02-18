import unittest

from programy.utils.geo.latlong import LatLong

#############################################################################
#

class LatLongTests(unittest.TestCase):

    def test_latlong(self):

        latlong = LatLong(latitude=1.0, longitude=2.0)
        self.assertIsNotNone(latlong)
        self.assertEqual(1.0, latlong.latitude)
        self.assertEqual(2.0, latlong.longitude)

        self.assertEqual("Latitude: 1.00, Longitude: 2.00", latlong.to_string())
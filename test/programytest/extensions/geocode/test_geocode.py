import unittest
from unittest.mock import patch
from programy.extensions.geocode.geocode import GeoCodeExtension
from programy.utils.geo.google import GoogleMaps
from programytest.client import TestClient


class MockGoogleMaps(GoogleMaps):

    response = None

    def _get_response_as_json(self, url):
        return MockGoogleMaps.response


class MockGeoCodeExtension(GeoCodeExtension):

    def __init__(self, geo_locator):
        self._geo_locator = geo_locator

    def get_geo_locator(self):
        return self._geo_locator


class GeoCodeExtensionTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        self.context = client.create_client_context("testid")
        MockGoogleMaps.response = {"results": [
                                                {
                                                  "address_components": [
                                                    {
                                                      "long_name": "KY3 9UR",
                                                      "short_name": "KY3 9UR",
                                                      "types": [
                                                        "postal_code"
                                                      ]
                                                    },
                                                    {
                                                      "long_name": "Glamis Road",
                                                      "short_name": "Glamis Rd",
                                                      "types": [
                                                        "route"
                                                      ]
                                                    },
                                                    {
                                                      "long_name": "Kinghorn",
                                                      "short_name": "Kinghorn",
                                                      "types": [
                                                        "locality",
                                                        "political"
                                                      ]
                                                    },
                                                    {
                                                      "long_name": "Burntisland",
                                                      "short_name": "Burntisland",
                                                      "types": [
                                                        "postal_town"
                                                      ]
                                                    },
                                                    {
                                                      "long_name": "Fife",
                                                      "short_name": "Fife",
                                                      "types": [
                                                        "administrative_area_level_2",
                                                        "political"
                                                      ]
                                                    },
                                                    {
                                                      "long_name": "Scotland",
                                                      "short_name": "Scotland",
                                                      "types": [
                                                        "administrative_area_level_1",
                                                        "political"
                                                      ]
                                                    },
                                                    {
                                                      "long_name": "United Kingdom",
                                                      "short_name": "GB",
                                                      "types": [
                                                        "country",
                                                        "political"
                                                      ]
                                                    }
                                                  ],
                                                  "formatted_address": "Glamis Rd, Kinghorn, Burntisland KY3 9UR, UK",
                                                  "geometry": {
                                                    "bounds": {
                                                      "northeast": {
                                                        "lat": 56.072498,
                                                        "lng": -3.1744103
                                                      },
                                                      "southwest": {
                                                        "lat": 56.071628,
                                                        "lng": -3.1757585
                                                      }
                                                    },
                                                    "location": {
                                                      "lat": 56.0720397,
                                                      "lng": -3.1752001
                                                    },
                                                    "location_type": "APPROXIMATE",
                                                    "viewport": {
                                                      "northeast": {
                                                        "lat": 56.0734119802915,
                                                        "lng": -3.173735419708498
                                                      },
                                                      "southwest": {
                                                        "lat": 56.0707140197085,
                                                        "lng": -3.176433380291502
                                                      }
                                                    }
                                                  },
                                                  "place_id": "ChIJT3l_Pwi2h0gRCp8egoK5hcU",
                                                  "types": [
                                                    "postal_code"
                                                  ]
                                                }
                                              ],
                                              "status": "OK"
                                            }

    def test_get_geo_locator(self):
        geocode = GeoCodeExtension()
        self.assertIsInstance(geocode.get_geo_locator(), GoogleMaps)

    def test_geocode_invalid(self):
        geo_locator = MockGoogleMaps()
        self.assertIsNotNone(geo_locator)
        geocode = MockGeoCodeExtension(geo_locator)
        self.assertIsNotNone(geocode)

        self.assertIsNone(geocode.execute(self.context, "POSTCODE1"))
        self.assertIsNone(geocode.execute(self.context, "POSTCODE1 XXX YYY"))
        self.assertIsNone(geocode.execute(self.context, "POSTCODE2 XXX"))
        self.assertIsNone(geocode.execute(self.context, "POSTCODE2 XXX YYY ZZZ"))
        self.assertIsNone(geocode.execute(self.context, "LOCATION"))
        self.assertIsNone(geocode.execute(self.context, "OTHER KINGHORN"))

    def test_geocode_postcode1(self):
        geo_locator = MockGoogleMaps()
        self.assertIsNotNone(geo_locator)
        geocode = MockGeoCodeExtension(geo_locator)
        self.assertIsNotNone(geocode)

        result = geocode.execute(self.context, "POSTCODE1 KY39UR")
        self.assertIsNotNone(result)
        self.assertEqual("LATITUDE DEC 56 FRAC 0720397 LONGITUDE DEC -3 FRAC 1752001", result)

    def test_geocode_postcode2(self):
        geo_locator = MockGoogleMaps()
        self.assertIsNotNone(geo_locator)
        geocode = MockGeoCodeExtension(geo_locator)
        self.assertIsNotNone(geocode)

        result = geocode.execute(self.context, "POSTCODE2 KY3 9UR")
        self.assertIsNotNone(result)
        self.assertEqual("LATITUDE DEC 56 FRAC 0720397 LONGITUDE DEC -3 FRAC 1752001", result)

    def test_geocode_location(self):
        geo_locator = MockGoogleMaps()
        self.assertIsNotNone(geo_locator)
        geocode = MockGeoCodeExtension(geo_locator)
        self.assertIsNotNone(geocode)

        result = geocode.execute(self.context, "LOCATION KINGHORN")
        self.assertIsNotNone(result)
        self.assertEqual("LATITUDE DEC 56 FRAC 0720397 LONGITUDE DEC -3 FRAC 1752001", result)

    def patch_get_latlong_for_location1(self, location):
        return None

    @patch("programy.utils.geo.google.GoogleMaps.get_latlong_for_location", patch_get_latlong_for_location1)
    def test_geocode_geocode_none(self):
        geocode = GeoCodeExtension()
        self.assertIsNotNone(geocode)
        self.assertIsNone(geocode.execute(self.context, "LOCATION KINGHORN"))

    def patch_get_latlong_for_location2(self, location):
        raise Exception("Mock Exception")

    @patch("programy.utils.geo.google.GoogleMaps.get_latlong_for_location", patch_get_latlong_for_location2)
    def test_geocode_geocode_exception(self):
        geocode = GeoCodeExtension()
        self.assertIsNotNone(geocode)
        self.assertIsNone(geocode.execute(self.context, "LOCATION KINGHORN"))
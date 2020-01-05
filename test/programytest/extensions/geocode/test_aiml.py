import json
import os
import unittest

from programy.extensions.geocode.geocode import GeoCodeExtension
from programy.utils.geo.google import GoogleMaps
from programytest.client import TestClient


class MockGoogleMaps(GoogleMaps):

    response = None

    def _get_response_as_json(self, url):
        return MockGoogleMaps.response


class MockGeoCodeExtension(GeoCodeExtension):

    def get_geo_locator(self):
        return MockGoogleMaps()


class GeoCodeTestsClient(TestClient):

    def __init__(self):
        TestClient.__init__(self, debug=True)

    def load_storage(self):
        super(GeoCodeTestsClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class GeoCodeAIMLTests(unittest.TestCase):

    LATLONG = None

    def setUp (self):
        client = GeoCodeTestsClient()
        self._client_context = client.create_client_context("testid")
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

    def test_postcode1(self):
        response =self._client_context.bot.ask_question(self._client_context, "POSTCODE KY39UR")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'LATITUDE DEC 56 FRAC 0720397 LONGITUDE DEC -3 FRAC 1752001.')

    def test_postcode2(self):
        response =self._client_context.bot.ask_question(self._client_context, "POSTCODE KY3 9UR")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'LATITUDE DEC 56 FRAC 0720397 LONGITUDE DEC -3 FRAC 1752001.')

    def test_location(self):
        response =self._client_context.bot.ask_question(self._client_context, "LOCATION KINGHORN")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'LATITUDE DEC 56 FRAC 0720397 LONGITUDE DEC -3 FRAC 1752001.')

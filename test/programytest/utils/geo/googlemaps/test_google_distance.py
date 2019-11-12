import json
import os
import unittest

from programy.utils.geo.google import GoogleMaps, GoogleDistance, GoogleDirections
from programy.utils.geo.latlong import LatLong


#############################################################################
#

class MockGoogleMaps(GoogleMaps):

    def __init__(self, response=None):
        self._response = response

    def _get_response_as_json(self, url):
        return self._response


class GoogleDistianceTests(unittest.TestCase):

    def test_distance_uk_driving_imperial(self):
        googlemaps = MockGoogleMaps(response={"destination_addresses": [
                                                "Kinghorn, UK"
                                              ],
                                              "origin_addresses": [
                                                "Edinburgh, UK"
                                              ],
                                              "rows": [
                                                {
                                                  "elements": [
                                                    {
                                                      "distance": {
                                                        "text": "25.1 mi",
                                                        "value": 40373
                                                      },
                                                      "duration": {
                                                        "text": "52 mins",
                                                        "value": 3097
                                                      },
                                                      "status": "OK"
                                                    }
                                                  ]
                                                }
                                              ],
                                              "status": "OK"
                                            })

        distance = googlemaps.get_distance_between_addresses("Edinburgh", "London", country="UK", mode="driving", units="imperial")
        self.assertIsNotNone(distance)
        self.assertIsInstance(distance, GoogleDistance)
        self.assertEqual("25.1 mi", distance._distance_text)

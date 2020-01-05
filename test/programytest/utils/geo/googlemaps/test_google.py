import unittest


from programy.utils.geo.google import GoogleDistance
from programy.utils.geo.google import GoogleMaps


class MockGoogleMaps(GoogleMaps):

    def __init__(self, content):
        GoogleMaps.__init__(self)
        self._content = content

    def _make_http_request(self, url):
        return self._content


class GoogleMapTests(unittest.TestCase):

    def test_googledistance(self):
        distance = GoogleDistance("origin", "destination", country="UK", mode="driving", units="imperial")
        distance.parse_json([{"elements": [
            {"distance": {
                "value": "9.99",
                "text": "testtext"},
             "duration": {
                 "value": "77",
                 "text": "testtext2"}
            }
        ]}])

    def test_googledistance_missing_elements(self):
        distance = GoogleDistance("origin", "destination", country="UK", mode="driving", units="imperial")
        with self.assertRaises(ValueError):
            distance.parse_json([{}])

    def test_googledistance_missing_distance(self):
        distance = GoogleDistance("origin", "destination", country="UK", mode="driving", units="imperial")
        with self.assertRaises(ValueError):
            distance.parse_json([{"elements": [
                {"duration": {
                     "value": "77",
                     "text": "testtext2"}
                }
            ]}])

    def test_googledistance_missing_duration(self):
        distance = GoogleDistance("origin", "destination", country="UK", mode="driving", units="imperial")
        with self.assertRaises(ValueError):
            distance.parse_json([{"elements": [
                {"distance": {
                    "value": "9.99",
                    "text": "testtext"}
                }
            ]}])

    def testis_error_response(self):
        googlemaps = MockGoogleMaps(None)

        self.assertTrue(googlemaps.is_error_response({"status": "OVER_QUERY_LIMIT"}))
        self.assertFalse(googlemaps.is_error_response({"status": "success"}))
        self.assertFalse(googlemaps.is_error_response({"xxxxxx": "success"}))

    def test_get_latlong_for_location(self):
        googlemaps = MockGoogleMaps({"results": [   {
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
        })
        self.assertIsNotNone(googlemaps)
        latlong = googlemaps.get_latlong_for_location("Edinburgh")
        self.assertIsNotNone(latlong)

    def test_get_latlong_for_location_no_location(self):
        googlemaps = MockGoogleMaps({"results": [   {
                                                        "address_components": [
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
        })
        self.assertIsNotNone(googlemaps)
        self.assertIsNotNone(googlemaps.get_latlong_for_location("Edinburgh"))

    def test_get_latlong_for_location_no_geometry(self):
        googlemaps = MockGoogleMaps({"results": [   {
                                                    }
                                                ],
            "status": "OK"
        })
        self.assertIsNotNone(googlemaps)
        with self.assertRaises(Exception):
            _ = googlemaps.get_latlong_for_location("Edinburgh")

    def test_get_latlong_for_location_geometry_no_location(self):
        googlemaps = MockGoogleMaps({"results": [   {
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
        })
        self.assertIsNotNone(googlemaps)
        loc = googlemaps.get_latlong_for_location("Edinburgh")
        self.assertIsNone(loc)

    def test_get_latlong_for_location_status_not_ok(self):
        googlemaps = MockGoogleMaps({"status": "OVER_QUERY_LIMIT"})
        self.assertIsNotNone(googlemaps)
        with self.assertRaises(Exception):
            _ = googlemaps.get_latlong_for_location("Edinburgh")

    def test_get_distance_between_addresses(self):
        googlemaps = MockGoogleMaps(content={"destination_addresses": [
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
        distance = googlemaps.get_distance_between_addresses("Edinburgh", "London")
        self.assertIsNotNone(distance)

    def test_get_distance_between_addresses_bad_status(self):
        googlemaps = MockGoogleMaps({"status": "OVER_QUERY_LIMIT"})
        self.assertIsNotNone(googlemaps)
        with self.assertRaises(Exception):
            _ = googlemaps.get_distance_between_addresses("Edinburgh", "London")

    def test_get_distance_between_addresses_status_not_ok(self):
        googlemaps = MockGoogleMaps({"status": "NOT OK"})
        self.assertIsNotNone(googlemaps)
        self.assertIsNone(googlemaps.get_distance_between_addresses("Edinburgh", "London"))

    def test_get_directions_between_addresses(self):
        googlemaps = MockGoogleMaps(content={"geocoded_waypoints": [
                                                {
                                                  "geocoder_status": "OK",
                                                  "place_id": "ChIJIyaYpQC4h0gRJxfnfHsU8mQ",
                                                  "types": [
                                                    "locality",
                                                    "political"
                                                  ]
                                                },
                                                {
                                                  "geocoder_status": "OK",
                                                  "place_id": "ChIJdyE-xuC1h0gR2qnGp00DIcA",
                                                  "types": [
                                                    "locality",
                                                    "political"
                                                  ]
                                                }
                                              ],
                                              "routes": [
                                                {
                                                  "bounds": {
                                                    "northeast": {
                                                      "lat": 56.0911029,
                                                      "lng": -3.1736554
                                                    },
                                                    "southwest": {
                                                      "lat": 55.9514313,
                                                      "lng": -3.4092736
                                                    }
                                                  },
                                                  "copyrights": "Map data \u00a92017 Google",
                                                  "legs": [
                                                    {
                                                      "distance": {
                                                        "text": "40.4 km",
                                                        "value": 40373
                                                      },
                                                      "duration": {
                                                        "text": "52 mins",
                                                        "value": 3098
                                                      },
                                                      "end_address": "Kinghorn, UK",
                                                      "end_location": {
                                                        "lat": 56.0712194,
                                                        "lng": -3.1742706
                                                      },
                                                      "start_address": "Edinburgh, UK",
                                                      "start_location": {
                                                        "lat": 55.9534595,
                                                        "lng": -3.1884629
                                                      },
                                                      "steps": [
                                                        {
                                                          "distance": {
                                                            "text": "0.4 km",
                                                            "value": 373
                                                          },
                                                          "duration": {
                                                            "text": "2 mins",
                                                            "value": 108
                                                          },
                                                          "end_location": {
                                                            "lat": 55.9564007,
                                                            "lng": -3.1868388
                                                          },
                                                          "html_instructions": "Head <b>west</b> on <b>Leith St</b>/<b>A900</b> toward <b>Leith St</b>/<b>A900</b>",
                                                          "polyline": {
                                                            "points": "clotIzvmRD^YAOCGCGCGCGEEEGGGKKSUa@EIAGSa@ISMUKQIKAAKKKMGIECSSo@QA?_Cg@e@KIAWAOAU?G@a@F"
                                                          },
                                                          "start_location": {
                                                            "lat": 55.9534595,
                                                            "lng": -3.1884629
                                                          },
                                                          "travel_mode": "DRIVING"
                                                        },
                                                        {
                                                          "distance": {
                                                            "text": "63 m",
                                                            "value": 63
                                                          },
                                                          "duration": {
                                                            "text": "1 min",
                                                            "value": 21
                                                          },
                                                          "end_location": {
                                                            "lat": 55.9566239,
                                                            "lng": -3.1876956
                                                          },
                                                          "html_instructions": "At the roundabout, take the <b>1st</b> exit onto <b>Broughton St</b>/<b>B901</b>",
                                                          "maneuver": "roundabout-left",
                                                          "polyline": {
                                                            "points": "o~otIvlmRCJABCBABCBC@C@Iv@Gp@A`@"
                                                          },
                                                          "start_location": {
                                                            "lat": 55.9564007,
                                                            "lng": -3.1868388
                                                          },
                                                          "travel_mode": "DRIVING"
                                                        },
                                                        {
                                                          "distance": {
                                                            "text": "75 m",
                                                            "value": 75
                                                          },
                                                          "duration": {
                                                            "text": "1 min",
                                                            "value": 16
                                                          },
                                                          "end_location": {
                                                            "lat": 56.0712194,
                                                            "lng": -3.1742706
                                                          },
                                                          "html_instructions": "Turn <b>right</b> onto <b>St Leonard's Pl</b>/<b>A921</b>",
                                                          "maneuver": "turn-right",
                                                          "polyline": {
                                                            "points": "wofuIjzjRh@n@h@t@^R"
                                                          },
                                                          "start_location": {
                                                            "lat": 56.07179989999999,
                                                            "lng": -3.1736554
                                                          },
                                                          "travel_mode": "DRIVING"
                                                        }
                                                      ],
                                                      "traffic_speed_entry": [],
                                                      "via_waypoint": []
                                                    }
                                                  ],
                                                  "overview_polyline": {
                                                    "points": "clotIzvmRD^YAWG]SwAqCkA}AcAe@aCg@wAQ]@e@RKNYlBAdBLrChCzXdGxm@tEhg@zArNQnAZp@N`A@l@@@BH?LA?NLtBdCJ]\\a@\\K`@Fl@`@gAhEcAtFkAnAmFtD_FvDa@z@YnA]rCd@xWh@v\\n@lZDPFAFFDZKRKfMIzKUvEiBfQ[fCqC|Q{@nH[xASzBSnLa@fD{@~CsDhMaHjUyBxHgBhIo@dFu@vHs@jJmAtQi@tJ{@vRm@vPB~Ll@`UnBv]pFf_AZjFd@hLAjJQxGg@vRI|HU~BeAxT_@jIa@xCy@vBoDjGeRxXi@v@Ib@g@~@gHbN_Pd_@gFtLyE|LuDfM_CjIgDhJuIzTkD~IsCpIuBnJyA~Lo@lMg@d|AFlSPlKvAtk@ZhFp@nE`C|MVxFUdIi@rLWrECxE_@nN{@bLeB~LwBbJ{BzGiBpEeBrCsB|CiCxCeCxBiEnCwDnAcGbA_FE}Tk@{oBgD}LOaCQeHAyEMcDOuC\\cBj@_CpA}LtIcKvGqCvAyBh@iEVqG?gKK_E@yEViGt@eGf@oBNeBP_@Z}@Zk@N{CJcBGyA[{@M[\\a@D_@SKc@SqBKmCBk@P]FqA}@qHYeC_@kHQoSI}FHqBh@aGb@oA?I@kAWmCGWDa@NMFBd@iAh@kGDwFWgHoBmRsEca@eBwQcAkQwAeLiGcX}AsFo@o@Ki@?iA]wCm@kDg@wEQyCMwGy@iGqJcp@oAgHw@qH{AiJyDeLy@{Bq@gCoByKYeBYmEi@kK[cK?{EwAgTqFgp@e@kHKkC]qBsAwNQsAMASe@g@Mc@[eEcDyAq@oKmCsM{CgTgFqAQwAe@kCsAoEcD{FoE{GoEoDwBwGqAgGOwAUaP}H}CsBiAFyB~@eAXiDkA}D}Am@k@k@iA]wBc@}J_@mJB}B`@_Gl@oIB_BKcBwFaa@}BwOoBs[i@mEyCgOa@qDOmEAkVu@sSs@mL_BuMoCcQ{EkSeFuQiGkUqBoJgGcf@eGwx@gDoc@}D}k@GyFd@gMpBm_@NqFAeDWiGY{EJMfFoFhCsCrAsBxBkDxEqHzEaIl@m@pAgCvDqIpF_LfDcDpAqDrBoGx@mEVyDv@mLr@}Ix@iDx@iBx@}A^sBj@{AlCgE`EwG~EcL`@sATGpAxBd@LTc@~BwHv@sDh@kEHSUaBh@a@d@_AlCqGZqAB{AKsE_AmFGmC@oAj@eA~@gAvA}BPUh@n@hAhA"
                                                  },
                                                  "summary": "A90",
                                                  "warnings": [],
                                                  "waypoint_order": []
                                                }
                                              ],
                                              "status": "OK"
                                            })
        directions = googlemaps.get_directions_between_addresses("Edinburgh", "London")
        self.assertIsNotNone(directions)

    def test_get_directions_between_addresses_bad_status(self):
        googlemaps = MockGoogleMaps({"status": "OVER_QUERY_LIMIT"})
        self.assertIsNotNone(googlemaps)
        with self.assertRaises(Exception):
            _ = googlemaps.get_directions_between_addresses("Edinburgh", "London")

    def test_get_directions_between_addresses_tatus_not_ok(self):
        googlemaps = MockGoogleMaps({"status": "NOTY_OK"})
        self.assertIsNotNone(googlemaps)
        self.assertIsNone(googlemaps.get_directions_between_addresses("Edinburgh", "London"))



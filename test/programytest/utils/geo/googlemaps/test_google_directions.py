import json
import os
import unittest

from programy.utils.geo.google import GoogleMaps, GoogleDistance, GoogleDirections
from programy.utils.geo.latlong import LatLong


#############################################################################
#

class MockGoogleMaps(GoogleMaps):

    def __init__(self, response):
        self._response = response

    def _get_response_as_json(self, url):
        return self._response


class GoogleDirectionsTests(unittest.TestCase):

    def test_directions(self):
        googlemaps = MockGoogleMaps(response={"geocoded_waypoints": [
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
        self.assertIsNotNone(googlemaps)

        directions = googlemaps.get_directions_between_addresses("Edinburgh", "London")
        self.assertIsNotNone(directions)
        self.assertIsInstance(directions, GoogleDirections)


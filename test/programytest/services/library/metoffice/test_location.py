import unittest
import metoffer
import datetime
from programy.services.library.metoffice.metoffice import Location
from programy.services.library.metoffice.metoffice import MetOfficeWeatherReport


class LocationTests(unittest.TestCase):

    def test_init(self):
        location = Location(MetOfficeWeatherReport.FORECAST, metoffer.DAILY)
        self.assertIsNotNone(location)

        self.assertEqual(MetOfficeWeatherReport.FORECAST, location._data_type)
        self.assertEqual(metoffer.DAILY, location._time_period)

        self.assertIsNotNone(location._reports)
        self.assertEqual([], location._reports)

        self.assertIsNone(location._continent)
        self.assertIsNone(location._country)
        self.assertIsNone(location._elevation)
        self.assertIsNone(location._i)
        self.assertIsNone(location._lat)
        self.assertIsNone(location._lon)
        self.assertIsNone(location._name)

        self.assertEquals(metoffer.DAILY, location.time_period)
        self.assertEquals(MetOfficeWeatherReport.FORECAST, location.data_type)

        self.assertIsNone(location.get_latest_report())
        self.assertIsNone(location.get_report_for_date("2017-04-03Z"))

    def test_parse_json(self):
        location = Location(MetOfficeWeatherReport.FORECAST, metoffer.DAILY)
        self.assertIsNotNone(location)

        json = {"Period": [{
                "Rep": [
                    {
                        "$": "Day",
                        "D": "S",
                        "Dm": "15",
                        "FDm": "13",
                        "Gn": "16",
                        "Hn": "54",
                        "PPd": "0",
                        "S": "9",
                        "U": "4",
                        "V": "VG",
                        "W": "1"
                    },
                    {
                        "$": "Night",
                        "D": "SSW",
                        "FNm": "7",
                        "Gm": "16",
                        "Hm": "86",
                        "Nm": "9",
                        "PPn": "57",
                        "S": "7",
                        "V": "GO",
                        "W": "7"
                    }
                ],
                "type": "Day",
                "value": "2017-04-03Z"
            },
            {
                "Rep": [
                    {
                        "$": "Day",
                        "D": "N",
                        "Dm": "13",
                        "FDm": "11",
                        "Gn": "11",
                        "Hn": "82",
                        "PPd": "49",
                        "S": "7",
                        "U": "2",
                        "V": "GO",
                        "W": "8"
                    },
                    {
                        "$": "Night",
                        "D": "NNW",
                        "FNm": "4",
                        "Gm": "11",
                        "Hm": "81",
                        "Nm": "5",
                        "PPn": "9",
                        "S": "4",
                        "V": "VG",
                        "W": "2"
                    }
                ],
                "type": "Day",
                "value": "2017-04-04Z"
            }
            ],
                "continent": "EUROPE",
                "country": "ENGLAND",
                "elevation": "4.0",
                "i": "351747",
                "lat": "51.4007",
                "lon": "-0.3337",
                "name": "HAMPTON COURT PALACE"
            }

        location.parse_json(json)

        self.assertIsNotNone(location._reports)
        self.assertEqual(2, len(location._reports))

        self.assertEqual("EUROPE", location._continent)
        self.assertEqual("ENGLAND", location._country)
        self.assertEqual("4.0", location._elevation)
        self.assertEqual("351747", location._i)
        self.assertEqual("51.4007", location._lat)
        self.assertEqual("-0.3337", location._lon)
        self.assertEqual("HAMPTON COURT PALACE", location._name)

        self.assertIsNotNone(location.get_latest_report())
        self.assertIsNotNone(location.get_report_for_date(datetime.datetime.strptime("2017-04-03Z", "%Y-%m-%dZ")))
        self.assertIsNone(location.get_report_for_date(datetime.datetime.strptime("2013-04-03Z", "%Y-%m-%dZ")))

    def test_parse_json_continent_missing(self):
        location = Location(MetOfficeWeatherReport.FORECAST, metoffer.DAILY)
        self.assertIsNotNone(location)

        json = {"Period": [],
            "country": "ENGLAND",
            "elevation": "4.0",
            "i": "351747",
            "lat": "51.4007",
            "lon": "-0.3337",
            "name": "HAMPTON COURT PALACE"
        }
        with self.assertRaises(ValueError):
            location.parse_json(json)

    def test_parse_json_missing_country(self):
        location = Location(MetOfficeWeatherReport.FORECAST, metoffer.DAILY)
        self.assertIsNotNone(location)

        json = {"Period": [
        ],
            "continent": "EUROPE",
            "elevation": "4.0",
            "i": "351747",
            "lat": "51.4007",
            "lon": "-0.3337",
            "name": "HAMPTON COURT PALACE"
        }
        with self.assertRaises(ValueError):
            location.parse_json(json)

    def test_parse_json_missing_elevation(self):
        location = Location(MetOfficeWeatherReport.FORECAST, metoffer.DAILY)
        self.assertIsNotNone(location)

        json = {"Period": [
        ],
            "continent": "EUROPE",
            "country": "ENGLAND",
            "i": "351747",
            "lat": "51.4007",
            "lon": "-0.3337",
            "name": "HAMPTON COURT PALACE"
        }
        with self.assertRaises(ValueError):
            location.parse_json(json)

    def test_parse_json_missing_i(self):
        location = Location(MetOfficeWeatherReport.FORECAST, metoffer.DAILY)
        self.assertIsNotNone(location)

        json = {"Period": [
        ],
            "continent": "EUROPE",
            "country": "ENGLAND",
            "elevation": "4.0",
            "lat": "51.4007",
            "lon": "-0.3337",
            "name": "HAMPTON COURT PALACE"
        }
        with self.assertRaises(ValueError):
            location.parse_json(json)

    def test_parse_json_missing_lat(self):
        location = Location(MetOfficeWeatherReport.FORECAST, metoffer.DAILY)
        self.assertIsNotNone(location)

        json = {"Period": [
        ],
            "continent": "EUROPE",
            "country": "ENGLAND",
            "elevation": "4.0",
            "i": "351747",
            "lon": "-0.3337",
            "name": "HAMPTON COURT PALACE"
        }
        with self.assertRaises(ValueError):
            location.parse_json(json)

    def test_parse_json_missing_lon(self):
        location = Location(MetOfficeWeatherReport.FORECAST, metoffer.DAILY)
        self.assertIsNotNone(location)

        json = {"Period": [
        ],
            "continent": "EUROPE",
            "country": "ENGLAND",
            "elevation": "4.0",
            "i": "351747",
            "lat": "51.4007",
            "name": "HAMPTON COURT PALACE"
        }
        with self.assertRaises(ValueError):
            location.parse_json(json)

    def test_parse_json_missing_name(self):
        location = Location(MetOfficeWeatherReport.FORECAST, metoffer.DAILY)
        self.assertIsNotNone(location)

        json = {"Period": [
        ],
            "continent": "EUROPE",
            "country": "ENGLAND",
            "elevation": "4.0",
            "i": "351747",
            "lat": "51.4007",
            "lon": "-0.3337",
        }
        with self.assertRaises(ValueError):
            location.parse_json(json)


import unittest
from programy.services.library.metoffice.metoffice import DailyForecastNightDataPoint


class DailyForecastNightDataPointTests(unittest.TestCase):

    def test_init(self):
        dp = DailyForecastNightDataPoint()
        self.assertIsNotNone(dp)

        self.assertIsNone(dp._type)
        self.assertIsNone(dp._wind_direction)
        self.assertIsNone(dp._temperature_feels_like_min)
        self.assertIsNone(dp._wind_gust_midnight)
        self.assertIsNone(dp._screen_relative_humidity_midnight)
        self.assertIsNone(dp._temp_min)
        self.assertIsNone(dp._precipitation_probability)
        self.assertIsNone(dp._wind_speed)
        self.assertIsNone(dp._visibility_code)
        self.assertIsNone(dp._visibility_text)
        self.assertIsNone(dp._weather_type_code)
        self.assertIsNone(dp._weather_type_text)

    def test_parse_json(self):
        dp = DailyForecastNightDataPoint()
        self.assertIsNotNone(dp)

        json = { "$": "Night",
                  "D": "SSW",
                  "FNm": "7",
                  "Gm": "16",
                  "Hm": "86",
                  "Nm": "9",
                  "PPn": "57",
                  "S": "7",
                  "V": "GO",
                  "W": "7"}

        dp.parse_json(json, "Night", "2017-04-03Z")

        self.assertEqual("Night", dp._type)
        self.assertEqual("SSW", dp._wind_direction)
        self.assertEqual("7", dp._temperature_feels_like_min)
        self.assertEqual("16", dp._wind_gust_midnight)
        self.assertEqual("86", dp._screen_relative_humidity_midnight)
        self.assertEqual("9", dp._temp_min)
        self.assertEqual("57", dp._precipitation_probability)
        self.assertEqual("7", dp._wind_speed)
        self.assertEqual("GO", dp._visibility_code)
        self.assertEqual("Good - Between 10-20 km", dp._visibility_text)
        self.assertEqual("7", dp._weather_type_code)
        self.assertEqual("Cloudy", dp._weather_type_text)

        self.assertEqual("WEATHER TYPE Cloudy WINDDIR SSW WINDGUST 16 WINDSPEED 7 TEMP 9 FEELS 7 HUMID 86 RAINPROB 57 VISTEXT Good - Between 10-20 km WEATHER Cloudy", dp.to_program_y_text())

    def test_parse_json_v_w_missing(self):
        dp = DailyForecastNightDataPoint()
        self.assertIsNotNone(dp)

        json = { "$": "Night",
                  "D": "SSW",
                  "FNm": "7",
                  "Gm": "16",
                  "Hm": "86",
                  "Nm": "9",
                  "PPn": "57",
                  "S": "7"}

        dp.parse_json(json, "Night", "2017-04-03Z")

        self.assertEqual("Night", dp._type)
        self.assertEqual("SSW", dp._wind_direction)
        self.assertEqual("7", dp._temperature_feels_like_min)
        self.assertEqual("16", dp._wind_gust_midnight)
        self.assertEqual("86", dp._screen_relative_humidity_midnight)
        self.assertEqual("9", dp._temp_min)
        self.assertEqual("57", dp._precipitation_probability)
        self.assertEqual("7", dp._wind_speed)
        self.assertEqual(None, dp._visibility_code)
        self.assertEqual(None, dp._visibility_text)
        self.assertEqual(None, dp._weather_type_code)
        self.assertEqual(None, dp._weather_type_text)

        self.assertEqual("WEATHER WINDDIR SSW WINDGUST 16 WINDSPEED 7 TEMP 9 FEELS 7 HUMID 86 RAINPROB 57", dp.to_program_y_text())


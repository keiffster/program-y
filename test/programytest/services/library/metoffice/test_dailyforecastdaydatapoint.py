import unittest
from programy.services.library.metoffice.metoffice import DailyForecastDayDataPoint


class DailyForecastDayDataPointTests(unittest.TestCase):

    def test_init(self):
        dp = DailyForecastDayDataPoint()
        self.assertIsNotNone(dp)

        self.assertIsNone(dp._type)
        self.assertIsNone(dp._wind_direction)
        self.assertIsNone(dp._temp_max)
        self.assertIsNone(dp._temperature_feels_like_max)
        self.assertIsNone(dp._wind_gust_noon)
        self.assertIsNone(dp._screen_relative_humidity_noon)
        self.assertIsNone(dp._precipitation_probability)
        self.assertIsNone(dp._wind_speed)
        self.assertIsNone(dp._uv_index_max)
        self.assertIsNone(dp._uv_guidance)
        self.assertIsNone(dp._visibility_code)
        self.assertIsNone(dp._visibility_text)
        self.assertIsNone(dp._weather_type_code)
        self.assertIsNone(dp._weather_type_text)

    def test_parse_json(self):
        dp = DailyForecastDayDataPoint()
        self.assertIsNotNone(dp)

        json = { "$": "Day",
                 "D": "S",
                 "Dm": "15",
                 "FDm": "13",
                 "Gn": "16",
                 "Hn": "54",
                 "PPd": "0",
                 "S": "9",
                 "U": "4",
                 "V": "VG",
                 "W": "1"}

        dp.parse_json(json, "Day", "2017-04-03Z")

        self.assertEqual("Day", dp._type)
        self.assertEqual("S", dp._wind_direction)
        self.assertEqual("15", dp._temp_max)
        self.assertEqual("13", dp._temperature_feels_like_max)
        self.assertEqual("16", dp._wind_gust_noon)
        self.assertEqual("54", dp._screen_relative_humidity_noon)
        self.assertEqual("0", dp._precipitation_probability)
        self.assertEqual("9", dp._wind_speed)
        self.assertEqual("4", dp._uv_index_max)
        self.assertEqual("Moderate exposure. Seek shade during midday hours, cover up and wear sunscreen", dp._uv_guidance)
        self.assertEqual("VG", dp._visibility_code)
        self.assertEqual("Very good - Between 20-40 km", dp._visibility_text)
        self.assertEqual("1", dp._weather_type_code)
        self.assertEqual("Sunny day", dp._weather_type_text )

        self.assertEqual("FORECAST DAYS TYPE Day WINDDIR S WINDSPEED 9 WINDGUST 16 TEMP 15 FEELS 13 HUMID 54 RAINPROB 0 UVINDEX 4 UVGUIDE Moderate exposure. Seek shade during midday hours, cover up and wear sunscreen VIS Very good - Between 20-40 km WEATHER Sunny day", dp.to_program_y_text())

    def test_parse_json_u_v_w_missing(self):
        dp = DailyForecastDayDataPoint()
        self.assertIsNotNone(dp)

        json = { "$": "Day",
                 "D": "S",
                 "Dm": "15",
                 "FDm": "13",
                 "Gn": "16",
                 "Hn": "54",
                 "PPd": "0",
                 "S": "9"}

        dp.parse_json(json, "Day", "2017-04-03Z")

        self.assertEqual("Day", dp._type)
        self.assertEqual("S", dp._wind_direction)
        self.assertEqual("15", dp._temp_max)
        self.assertEqual("13", dp._temperature_feels_like_max)
        self.assertEqual("16", dp._wind_gust_noon)
        self.assertEqual("54", dp._screen_relative_humidity_noon)
        self.assertEqual("0", dp._precipitation_probability)
        self.assertEqual("9", dp._wind_speed)
        self.assertEqual(None, dp._uv_index_max)
        self.assertEqual(None, dp._uv_guidance)
        self.assertEqual(None, dp._visibility_code)
        self.assertEqual(None, dp._visibility_text)
        self.assertEqual(None, dp._weather_type_code)
        self.assertEqual(None, dp._weather_type_text )

        self.assertEqual("FORECAST DAYS TYPE Day WINDDIR S WINDSPEED 9 WINDGUST 16 TEMP 15 FEELS 13 HUMID 54 RAINPROB 0", dp.to_program_y_text())

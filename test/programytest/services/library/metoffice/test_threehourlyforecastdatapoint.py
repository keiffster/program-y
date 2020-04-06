import unittest
from programy.services.library.metoffice.metoffice import ThreeHourlyForecastDataPoint


class ThreeHourlyForecastDataPointTests(unittest.TestCase):

    def test_init(self):
        dp = ThreeHourlyForecastDataPoint()
        self.assertIsNotNone(dp)

        self.assertIsNone(dp._time)
        self.assertIsNone(dp._weather_type_code)
        self.assertIsNone(dp._weather_type_text)
        self.assertIsNone(dp._temperature)
        self.assertIsNone(dp._temperature_feels_like)
        self.assertIsNone(dp._wind_gust)
        self.assertIsNone(dp._wind_direction)
        self.assertIsNone(dp._wind_direction_full)
        self.assertIsNone(dp._wind_speed)
        self.assertIsNone(dp._visibility_code)
        self.assertIsNone(dp._visibility_text)
        self.assertIsNone(dp._uv_index_max)
        self.assertIsNone(dp._uv_guidance)
        self.assertIsNone(dp._precipitation_probability)
        self.assertIsNone(dp._screen_relative_humidity)

    def test_parse_json(self):
        dp = ThreeHourlyForecastDataPoint()
        self.assertIsNotNone(dp)

        json = {  "$": "360",
                  "D": "S",
                  "F": "3",
                  "G": "4",
                  "H": "96",
                  "Pp": "0",
                  "S": "2",
                  "T": "4",
                  "U": "1",
                  "V": "MO",
                  "W": "1"}

        dp.parse_json(json, "360", "2017-04-03Z")

        self.assertEqual("360", dp._time)
        self.assertEqual("1", dp._weather_type_code)
        self.assertEqual("Sunny day", dp._weather_type_text)
        self.assertEqual("4", dp._temperature)
        self.assertEqual("3", dp._temperature_feels_like)
        self.assertEqual("4", dp._wind_gust)
        self.assertEqual("S", dp._wind_direction)
        self.assertEqual("South", dp._wind_direction_full)
        self.assertEqual("2", dp._wind_speed)
        self.assertEqual("MO", dp._visibility_code)
        self.assertEqual("Moderate - Between 4-10 km", dp._visibility_text)
        self.assertEqual("1", dp._uv_index_max)
        self.assertEqual("Low exposure. No protection required. You can safely stay outside", dp._uv_guidance)
        self.assertEqual("0", dp._precipitation_probability)
        self.assertEqual("96", dp._screen_relative_humidity)

        self.assertEqual("FORECAST HOURS TYPE Sunny day TEMP 4 FEELS 3 WINDSPEED 2 UVINDEX 1 UVGUIDE Low exposure. No protection required. You can safely stay outside RAINPROB 0 HUMIDITY 96 WINDDIR S WINDDIRFULL South VIS Moderate - Between 4-10 km", dp.to_program_y_text())

    def test_parse_json_s_u_v_w_missing(self):
        dp = ThreeHourlyForecastDataPoint()
        self.assertIsNotNone(dp)

        json = {  "$": "360",
                  "S": "2",
                  "F": "3",
                  "G": "4",
                  "H": "96",
                  "Pp": "0",
                  "T": "4"}

        dp.parse_json(json, "360", "2017-04-03Z")

        self.assertEqual("360", dp._time)
        self.assertEqual(None, dp._weather_type_code)
        self.assertEqual(None, dp._weather_type_text)
        self.assertEqual("4", dp._temperature)
        self.assertEqual("3", dp._temperature_feels_like)
        self.assertEqual("4", dp._wind_gust)
        self.assertEqual(None, dp._wind_direction)
        self.assertEqual(None, dp._wind_direction_full)
        self.assertEqual("2", dp._wind_speed)
        self.assertEqual(None, dp._visibility_code)
        self.assertEqual(None, dp._visibility_text)
        self.assertEqual(None, dp._uv_index_max)
        self.assertEqual(None, dp._uv_guidance)
        self.assertEqual("0", dp._precipitation_probability)
        self.assertEqual("96", dp._screen_relative_humidity)

        self.assertEqual("FORECAST HOURS TEMP 4 FEELS 3 WINDSPEED 2 UVINDEX None UVGUIDE None RAINPROB 0 HUMIDITY 96", dp.to_program_y_text())

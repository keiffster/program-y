import unittest
from programy.services.library.metoffice.metoffice import ObservationDataPoint


class ObservationDataPointTests(unittest.TestCase):

    def test_init(self):
        dp = ObservationDataPoint()
        self.assertIsNotNone(dp)

        self.assertIsNone(dp._time)
        self.assertIsNone(dp._temperature)
        self.assertIsNone(dp._visibility)
        self.assertIsNone(dp._visibility_text)
        self.assertIsNone(dp._wind_direction)
        self.assertIsNone(dp._wind_direction_full)
        self.assertIsNone(dp._wind_speed)
        self.assertIsNone(dp._weather_type_code)
        self.assertIsNone(dp._weather_type_text)
        self.assertIsNone(dp._pressure)
        self.assertIsNone(dp._pressure_tendancy)
        self.assertIsNone(dp._pressure_tendancy_full)
        self.assertIsNone(dp._dew_point)
        self.assertIsNone(dp._screen_relative_humidity)

    def test_parse_json(self):
        dp = ObservationDataPoint()
        self.assertIsNotNone(dp)

        json = {
            "$": "660",
            "D": "W",
            "Dp": "3.2",
            "H": "57.3",
            "P": "1021",
            "Pt": "R",
            "S": "11",
            "T": "11.2",
            "V": "35000",
            "W": "3"
        }

        dp.parse_json(json, "Day", "660")

        self.assertEqual("660", dp._time)
        self.assertEqual("11.2", dp._temperature)
        self.assertEqual("35000", dp._visibility)
        self.assertEqual("Very Good", dp._visibility_text)
        self.assertEqual("W", dp._wind_direction)
        self.assertEqual("West", dp._wind_direction_full)
        self.assertEqual("11", dp._wind_speed)
        self.assertEqual("3", dp._weather_type_code)
        self.assertEqual("Partly cloudy (day)", dp._weather_type_text)
        self.assertEqual("1021", dp._pressure)
        self.assertEqual("R", dp._pressure_tendancy)
        self.assertEqual("Rising", dp._pressure_tendancy_full)
        self.assertEqual("3.2", dp._dew_point)
        self.assertEqual("57.3", dp._screen_relative_humidity)

        self.assertEqual("OBSERVATION TYPE Partly cloudy (day) TEMP PLUS 11 2 HUMIDITY 57 3 VISIBILITY V 35000 VF Very Good PRESSURE P 1021 PT R PTF Rising WIND D W DF West S 11", dp.to_program_y_text())

    def test_parse_json_V_D_W_Pt(self):
        dp = ObservationDataPoint()
        self.assertIsNotNone(dp)

        json = {
            "$": "660",
            "Dp": "3.2",
            "H": "57.3",
            "P": "1021",
            "S": "11",
            "T": "11.2"
        }

        dp.parse_json(json, "Day", "660")

        self.assertEqual("660", dp._time)
        self.assertEqual("11.2", dp._temperature)
        self.assertEqual(None, dp._visibility)
        self.assertEqual(None, dp._visibility_text)
        self.assertEqual(None, dp._wind_direction)
        self.assertEqual(None, dp._wind_direction_full)
        self.assertEqual("11", dp._wind_speed)
        self.assertEqual(None, dp._weather_type_code)
        self.assertEqual(None, dp._weather_type_text)
        self.assertEqual("1021", dp._pressure)
        self.assertEqual(None, dp._pressure_tendancy)
        self.assertEqual(None, dp._pressure_tendancy_full)
        self.assertEqual("3.2", dp._dew_point)
        self.assertEqual("57.3", dp._screen_relative_humidity)

        self.assertEqual("OBSERVATION TEMP PLUS 11 2 HUMIDITY 57 3 PRESSURE P 1021 S 11", dp.to_program_y_text())

    def test_parse_visibility_to_text(self):
        dp = ObservationDataPoint()
        self.assertIsNotNone(dp)

        self.assertEqual("Very poor", dp.parse_visibility_to_text(99))

        self.assertEqual("Poor", dp.parse_visibility_to_text(1000))
        self.assertEqual("Poor", dp.parse_visibility_to_text(3999))

        self.assertEqual("Moderate", dp.parse_visibility_to_text(4000))
        self.assertEqual("Moderate", dp.parse_visibility_to_text(9999))

        self.assertEqual("Good", dp.parse_visibility_to_text(10000))
        self.assertEqual("Good", dp.parse_visibility_to_text(19999))

        self.assertEqual("Very Good", dp.parse_visibility_to_text(20000))
        self.assertEqual("Very Good", dp.parse_visibility_to_text(39999))

        self.assertEqual("Excellent", dp.parse_visibility_to_text(40000))
        self.assertEqual("Excellent", dp.parse_visibility_to_text(99999999))

    def test_parse_pressure_tendancy(self):
        dp = ObservationDataPoint()
        self.assertIsNotNone(dp)

        self.assertEqual("Rising", dp.parse_pressure_tendancy('R'))
        self.assertEqual("Falling", dp.parse_pressure_tendancy('F'))

        self.assertEqual("Unknown", dp.parse_pressure_tendancy(None))
        self.assertEqual("Unknown", dp.parse_pressure_tendancy(''))
        self.assertEqual("Unknown", dp.parse_pressure_tendancy('X'))


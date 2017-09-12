import unittest
import os
import datetime
import metoffer

from programy.utils.weather.metoffice import DataPoint
from programy.utils.weather.metoffice import DailyForecastDayDataPoint
from programy.utils.weather.metoffice import DailyForecastNightDataPoint
from programy.utils.weather.metoffice import ThreeHourlyForecastDataPoint
from programy.utils.weather.metoffice import ObservationDataPoint
from programy.utils.weather.metoffice import Report
from programy.utils.weather.metoffice import Location
from programy.utils.weather.metoffice import DV
from programy.utils.weather.metoffice import SiteReport
from programy.utils.weather.metoffice import MetOfficeWeatherReport
from programy.utils.weather.metoffice import MetOffice
from programy.utils.text.dateformat import DateFormatter
from programy.utils.license.keys import LicenseKeys

class DataPointTets(unittest.TestCase):

    def test_init(self):
        dp = DataPoint()
        self.assertIsNotNone(dp)

    def test_extract_attribute(self):
        dp = DataPoint()
        self.assertIsNotNone(dp)

        self.assertEquals("value", dp.extract_attribute({"item": "value"}, "item", MetOfficeWeatherReport.ObservationDataPoint))
        self.assertIsNone(dp.extract_attribute({"item": "value"}, "itemx", MetOfficeWeatherReport.ObservationDataPoint, None))

        self.assertEquals("value", dp.extract_attribute({"item": "value"}, "item", MetOfficeWeatherReport.FORECAST, metoffer.THREE_HOURLY))
        self.assertIsNone(dp.extract_attribute({"item": "value"}, "itemx", MetOfficeWeatherReport.FORECAST, metoffer.THREE_HOURLY))

        self.assertEquals("value", dp.extract_attribute({"item": "value"}, "item", MetOfficeWeatherReport.FORECAST,metoffer.DAILY))
        self.assertIsNone(dp.extract_attribute({"item": "value"}, "itemx", MetOfficeWeatherReport.FORECAST,metoffer.DAILY))

        self.assertIsNone(dp.extract_attribute({"item": "value"}, "itemx", 3))

    def test_direction_to_full_text(self):
        dp = DataPoint()
        self.assertIsNotNone(dp)

        self.assertEquals(dp.direction_to_full_text('N'), 'North')
        self.assertEquals(dp.direction_to_full_text('NNE'), 'North North East')
        self.assertEquals(dp.direction_to_full_text('NE'), 'North East')
        self.assertEquals(dp.direction_to_full_text('ENE'), 'East North East')
        self.assertEquals(dp.direction_to_full_text('E'), 'East')
        self.assertEquals(dp.direction_to_full_text('ESE'), 'East South East')
        self.assertEquals(dp.direction_to_full_text('SE'), 'South East')
        self.assertEquals(dp.direction_to_full_text('SSE'), 'South South East')
        self.assertEquals(dp.direction_to_full_text('S'), 'South')
        self.assertEquals(dp.direction_to_full_text('SSW'), 'South South West')
        self.assertEquals(dp.direction_to_full_text('SW'), 'South West')
        self.assertEquals(dp.direction_to_full_text('WSW'), 'West South West')
        self.assertEquals(dp.direction_to_full_text('W'), 'West')
        self.assertEquals(dp.direction_to_full_text('WNW'), 'West North West')
        self.assertEquals(dp.direction_to_full_text('NW'), 'North West')
        self.assertEquals(dp.direction_to_full_text('NNW'), 'North North West')

        self.assertEquals(dp.direction_to_full_text(''), "Unknown")
        self.assertEquals(dp.direction_to_full_text('other'), "Unknown")
        self.assertEquals(dp.direction_to_full_text(None), "Unknown")

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
        self.assertIsNone(dp._weather_type_text )

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

        self.assertEquals("WEATHER Sunny day", dp.to_program_y_text())

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

        self.assertEquals("WEATHER Cloudy", dp.to_program_y_text())

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

        self.assertEquals("WEATHER Sunny day TEMP 4 TF 3 WIND D S F South S 2 VISIBILITY Moderate - Between 4-10 km UV I 1 G Low exposure. No protection required. You can safely stay outside RAIN 0 HUMIDITY 96", dp.to_program_y_text())

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

        self.assertEquals("WEATHER Partly cloudy (day) TEMP 11 2 VISIBILITY V 35000 VF Very Good WIND D W DF West S 11 PRESSURE P 1021 PT R PTF Rising HUMIDITY 57 3", dp.to_program_y_text())

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

class ReportTests(unittest.TestCase):

    def test_init(self):
        report = Report("Forecast", "2017-04-03T09:00:00Z")
        self.assertIsNotNone(report)

        self.assertEquals("Forecast", report._data_type)
        self.assertEquals("2017-04-03T09:00:00Z", report._time_period)

        self.assertIsNotNone(report._time_periods)
        self.assertEquals([], report._time_periods)

        self.assertIsNone(report._type)
        self.assertIsNone(report._report_date)

    def test_parse_json(self):
        report = Report(MetOfficeWeatherReport.FORECAST, metoffer.DAILY)
        self.assertIsNotNone(report)

        json = { "Rep": [ { "$": "Day",
                          "D": "S",
                          "Dm": "15",
                          "FDm": "13",
                          "Gn": "16",
                          "Hn": "54",
                          "PPd": "0",
                          "S": "9",
                          "U": "4",
                          "V": "VG",
                          "W": "1"},
                        { "$": "Night",
                          "D": "SSW",
                          "FNm": "7",
                          "Gm": "16",
                          "Hm": "86",
                          "Nm": "9",
                          "PPn": "57",
                          "S": "7",
                          "V": "GO",
                          "W": "7"}],
               "type": "Day",
               "value": "2017-04-03Z"}
        report.parse_json(json)

        self.assertEqual(report._data_type, MetOfficeWeatherReport.FORECAST)
        self.assertEqual(report._time_period, metoffer.DAILY)

        self.assertEqual(2, len(report._time_periods))

        self.assertEqual(report._type, "Day")
        self.assertEqual(report._report_date, datetime.datetime(2017, 4, 3, 0, 0))


class LocationTests(unittest.TestCase):

    def test_init(self):
        location = Location(MetOfficeWeatherReport.FORECAST, metoffer.DAILY)
        self.assertIsNotNone(location)

        self.assertEquals(MetOfficeWeatherReport.FORECAST, location._data_type)
        self.assertEquals(metoffer.DAILY, location._time_period)

        self.assertIsNotNone(location._reports)
        self.assertEquals([], location._reports)

        self.assertIsNone(location._continent)
        self.assertIsNone(location._country)
        self.assertIsNone(location._elevation)
        self.assertIsNone(location._i)
        self.assertIsNone(location._lat)
        self.assertIsNone(location._lon)
        self.assertIsNone(location._name)

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
        self.assertEquals(2, len(location._reports))

        self.assertEqual("EUROPE", location._continent)
        self.assertEqual("ENGLAND", location._country)
        self.assertEqual("4.0", location._elevation)
        self.assertEqual("351747", location._i)
        self.assertEqual("51.4007", location._lat)
        self.assertEqual("-0.3337", location._lon)
        self.assertEqual("HAMPTON COURT PALACE", location._name)


class DVTests(unittest.TestCase):

    def test_init(self):
        dv = DV(MetOfficeWeatherReport.FORECAST, metoffer.DAILY)
        self.assertIsNotNone(dv)

        self.assertEquals(MetOfficeWeatherReport.FORECAST, dv._data_type)
        self.assertEquals(metoffer.DAILY, dv._time_period)

        self.assertIsNone(dv._date)
        self.assertIsNone(dv._type)
        self.assertIsNone(dv._location)

    def test_parse_json(self):
        dv = DV(MetOfficeWeatherReport.FORECAST, metoffer.DAILY)
        self.assertIsNotNone(dv)

        json = {
              "Location": {
                "Period": [
                  {
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
                  },
                  {
                    "Rep": [
                      {
                        "$": "Day",
                        "D": "NW",
                        "Dm": "12",
                        "FDm": "10",
                        "Gn": "20",
                        "Hn": "59",
                        "PPd": "9",
                        "S": "11",
                        "U": "3",
                        "V": "VG",
                        "W": "8"
                      },
                      {
                        "$": "Night",
                        "D": "NNW",
                        "FNm": "6",
                        "Gm": "11",
                        "Hm": "79",
                        "Nm": "6",
                        "PPn": "8",
                        "S": "7",
                        "V": "VG",
                        "W": "7"
                      }
                    ],
                    "type": "Day",
                    "value": "2017-04-05Z"
                  },
                  {
                    "Rep": [
                      {
                        "$": "Day",
                        "D": "WNW",
                        "Dm": "14",
                        "FDm": "13",
                        "Gn": "11",
                        "Hn": "61",
                        "PPd": "8",
                        "S": "4",
                        "U": "4",
                        "V": "VG",
                        "W": "7"
                      },
                      {
                        "$": "Night",
                        "D": "NW",
                        "FNm": "7",
                        "Gm": "9",
                        "Hm": "81",
                        "Nm": "7",
                        "PPn": "10",
                        "S": "4",
                        "V": "VG",
                        "W": "8"
                      }
                    ],
                    "type": "Day",
                    "value": "2017-04-06Z"
                  },
                  {
                    "Rep": [
                      {
                        "$": "Day",
                        "D": "WNW",
                        "Dm": "13",
                        "FDm": "12",
                        "Gn": "11",
                        "Hn": "66",
                        "PPd": "11",
                        "S": "4",
                        "U": "3",
                        "V": "VG",
                        "W": "8"
                      },
                      {
                        "$": "Night",
                        "D": "NW",
                        "FNm": "8",
                        "Gm": "7",
                        "Hm": "76",
                        "Nm": "8",
                        "PPn": "8",
                        "S": "4",
                        "V": "VG",
                        "W": "7"
                      }
                    ],
                    "type": "Day",
                    "value": "2017-04-07Z"
                  }
                ],
                "continent": "EUROPE",
                "country": "ENGLAND",
                "elevation": "4.0",
                "i": "351747",
                "lat": "51.4007",
                "lon": "-0.3337",
                "name": "HAMPTON COURT PALACE"
              },
              "dataDate": "2017-04-03T09:00:00Z",
              "type": "Forecast"
            }

        dv.parse_json(json)

        self.assertEqual(datetime.datetime(2017, 4, 3, 9, 0), dv._date)
        self.assertEqual("Forecast", dv._type)
        self.assertIsNotNone("", dv._location)


class SiteReportTests(unittest.TestCase):

    def test_init(self):
        report = SiteReport(MetOfficeWeatherReport.FORECAST, metoffer.DAILY)
        self.assertIsNotNone(report)

        self.assertEquals(MetOfficeWeatherReport.FORECAST, report._data_type)
        self.assertEquals(metoffer.DAILY, report._time_period)

        self.assertIsNone(report._dv)

    def test_parse_json(self):
        report = SiteReport(MetOfficeWeatherReport.FORECAST, metoffer.DAILY)
        self.assertIsNotNone(report)

        json = {
                "DV": {
                    "Location": {
                        "Period": [
                            {
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
                            },
                            {
                                "Rep": [
                                    {
                                        "$": "Day",
                                        "D": "NW",
                                        "Dm": "12",
                                        "FDm": "10",
                                        "Gn": "20",
                                        "Hn": "59",
                                        "PPd": "9",
                                        "S": "11",
                                        "U": "3",
                                        "V": "VG",
                                        "W": "8"
                                    },
                                    {
                                        "$": "Night",
                                        "D": "NNW",
                                        "FNm": "6",
                                        "Gm": "11",
                                        "Hm": "79",
                                        "Nm": "6",
                                        "PPn": "8",
                                        "S": "7",
                                        "V": "VG",
                                        "W": "7"
                                    }
                                ],
                                "type": "Day",
                                "value": "2017-04-05Z"
                            },
                            {
                                "Rep": [
                                    {
                                        "$": "Day",
                                        "D": "WNW",
                                        "Dm": "14",
                                        "FDm": "13",
                                        "Gn": "11",
                                        "Hn": "61",
                                        "PPd": "8",
                                        "S": "4",
                                        "U": "4",
                                        "V": "VG",
                                        "W": "7"
                                    },
                                    {
                                        "$": "Night",
                                        "D": "NW",
                                        "FNm": "7",
                                        "Gm": "9",
                                        "Hm": "81",
                                        "Nm": "7",
                                        "PPn": "10",
                                        "S": "4",
                                        "V": "VG",
                                        "W": "8"
                                    }
                                ],
                                "type": "Day",
                                "value": "2017-04-06Z"
                            },
                            {
                                "Rep": [
                                    {
                                        "$": "Day",
                                        "D": "WNW",
                                        "Dm": "13",
                                        "FDm": "12",
                                        "Gn": "11",
                                        "Hn": "66",
                                        "PPd": "11",
                                        "S": "4",
                                        "U": "3",
                                        "V": "VG",
                                        "W": "8"
                                    },
                                    {
                                        "$": "Night",
                                        "D": "NW",
                                        "FNm": "8",
                                        "Gm": "7",
                                        "Hm": "76",
                                        "Nm": "8",
                                        "PPn": "8",
                                        "S": "4",
                                        "V": "VG",
                                        "W": "7"
                                    }
                                ],
                                "type": "Day",
                                "value": "2017-04-07Z"
                            }
                        ],
                        "continent": "EUROPE",
                        "country": "ENGLAND",
                        "elevation": "4.0",
                        "i": "351747",
                        "lat": "51.4007",
                        "lon": "-0.3337",
                        "name": "HAMPTON COURT PALACE"
                    },
                    "dataDate": "2017-04-03T09:00:00Z",
                    "type": "Forecast"
                },
                "Wx": {
                    "Param": [
                        {
                            "$": "Feels Like Day Maximum Temperature",
                            "name": "FDm",
                            "units": "C"
                        },
                        {
                            "$": "Feels Like Night Minimum Temperature",
                            "name": "FNm",
                            "units": "C"
                        },
                        {
                            "$": "Day Maximum Temperature",
                            "name": "Dm",
                            "units": "C"
                        },
                        {
                            "$": "Night Minimum Temperature",
                            "name": "Nm",
                            "units": "C"
                        },
                        {
                            "$": "Wind Gust Noon",
                            "name": "Gn",
                            "units": "mph"
                        },
                        {
                            "$": "Wind Gust Midnight",
                            "name": "Gm",
                            "units": "mph"
                        },
                        {
                            "$": "Screen Relative Humidity Noon",
                            "name": "Hn",
                            "units": "%"
                        },
                        {
                            "$": "Screen Relative Humidity Midnight",
                            "name": "Hm",
                            "units": "%"
                        },
                        {
                            "$": "Visibility",
                            "name": "V",
                            "units": ""
                        },
                        {
                            "$": "Wind Direction",
                            "name": "D",
                            "units": "compass"
                        },
                        {
                            "$": "Wind Speed",
                            "name": "S",
                            "units": "mph"
                        },
                        {
                            "$": "Max UV Index",
                            "name": "U",
                            "units": ""
                        },
                        {
                            "$": "Weather Type",
                            "name": "W",
                            "units": ""
                        },
                        {
                            "$": "Precipitation Probability Day",
                            "name": "PPd",
                            "units": "%"
                        },
                        {
                            "$": "Precipitation Probability Night",
                            "name": "PPn",
                            "units": "%"
                        }
                    ]
                }
            }

        report.parse_json(json)

        self.assertEquals(MetOfficeWeatherReport.FORECAST, report._data_type)
        self.assertEquals(metoffer.DAILY, report._time_period)
        self.assertIsNotNone("", report._dv)

class MetOfficeWeatherReportTests(unittest.TestCase):

    def test_init(self):
        report = MetOfficeWeatherReport(MetOfficeWeatherReport.FORECAST)
        self.assertIsNotNone(report)

        self.assertEquals(MetOfficeWeatherReport.FORECAST, report._data_type)
        self.assertEquals(0, report._time_period)
        self.assertIsNone(report._site_report)

    def test_init_with_timeperiod(self):
        report = MetOfficeWeatherReport(MetOfficeWeatherReport.FORECAST, metoffer.DAILY)
        self.assertIsNotNone(report)

        self.assertEquals(MetOfficeWeatherReport.FORECAST, report._data_type)
        self.assertEquals(metoffer.DAILY, report._time_period)
        self.assertIsNone(report._site_report)

    def test_parse_json(self):
        report = MetOfficeWeatherReport(MetOfficeWeatherReport.FORECAST, metoffer.DAILY)
        self.assertIsNotNone(report)

        json = {
            "SiteRep": {
                "DV": {
                    "Location": {
                        "Period": [
                            {
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
                            },
                            {
                                "Rep": [
                                    {
                                        "$": "Day",
                                        "D": "NW",
                                        "Dm": "12",
                                        "FDm": "10",
                                        "Gn": "20",
                                        "Hn": "59",
                                        "PPd": "9",
                                        "S": "11",
                                        "U": "3",
                                        "V": "VG",
                                        "W": "8"
                                    },
                                    {
                                        "$": "Night",
                                        "D": "NNW",
                                        "FNm": "6",
                                        "Gm": "11",
                                        "Hm": "79",
                                        "Nm": "6",
                                        "PPn": "8",
                                        "S": "7",
                                        "V": "VG",
                                        "W": "7"
                                    }
                                ],
                                "type": "Day",
                                "value": "2017-04-05Z"
                            },
                            {
                                "Rep": [
                                    {
                                        "$": "Day",
                                        "D": "WNW",
                                        "Dm": "14",
                                        "FDm": "13",
                                        "Gn": "11",
                                        "Hn": "61",
                                        "PPd": "8",
                                        "S": "4",
                                        "U": "4",
                                        "V": "VG",
                                        "W": "7"
                                    },
                                    {
                                        "$": "Night",
                                        "D": "NW",
                                        "FNm": "7",
                                        "Gm": "9",
                                        "Hm": "81",
                                        "Nm": "7",
                                        "PPn": "10",
                                        "S": "4",
                                        "V": "VG",
                                        "W": "8"
                                    }
                                ],
                                "type": "Day",
                                "value": "2017-04-06Z"
                            },
                            {
                                "Rep": [
                                    {
                                        "$": "Day",
                                        "D": "WNW",
                                        "Dm": "13",
                                        "FDm": "12",
                                        "Gn": "11",
                                        "Hn": "66",
                                        "PPd": "11",
                                        "S": "4",
                                        "U": "3",
                                        "V": "VG",
                                        "W": "8"
                                    },
                                    {
                                        "$": "Night",
                                        "D": "NW",
                                        "FNm": "8",
                                        "Gm": "7",
                                        "Hm": "76",
                                        "Nm": "8",
                                        "PPn": "8",
                                        "S": "4",
                                        "V": "VG",
                                        "W": "7"
                                    }
                                ],
                                "type": "Day",
                                "value": "2017-04-07Z"
                            }
                        ],
                        "continent": "EUROPE",
                        "country": "ENGLAND",
                        "elevation": "4.0",
                        "i": "351747",
                        "lat": "51.4007",
                        "lon": "-0.3337",
                        "name": "HAMPTON COURT PALACE"
                    },
                    "dataDate": "2017-04-03T09:00:00Z",
                    "type": "Forecast"
                },
                "Wx": {
                    "Param": [
                        {
                            "$": "Feels Like Day Maximum Temperature",
                            "name": "FDm",
                            "units": "C"
                        },
                        {
                            "$": "Feels Like Night Minimum Temperature",
                            "name": "FNm",
                            "units": "C"
                        },
                        {
                            "$": "Day Maximum Temperature",
                            "name": "Dm",
                            "units": "C"
                        },
                        {
                            "$": "Night Minimum Temperature",
                            "name": "Nm",
                            "units": "C"
                        },
                        {
                            "$": "Wind Gust Noon",
                            "name": "Gn",
                            "units": "mph"
                        },
                        {
                            "$": "Wind Gust Midnight",
                            "name": "Gm",
                            "units": "mph"
                        },
                        {
                            "$": "Screen Relative Humidity Noon",
                            "name": "Hn",
                            "units": "%"
                        },
                        {
                            "$": "Screen Relative Humidity Midnight",
                            "name": "Hm",
                            "units": "%"
                        },
                        {
                            "$": "Visibility",
                            "name": "V",
                            "units": ""
                        },
                        {
                            "$": "Wind Direction",
                            "name": "D",
                            "units": "compass"
                        },
                        {
                            "$": "Wind Speed",
                            "name": "S",
                            "units": "mph"
                        },
                        {
                            "$": "Max UV Index",
                            "name": "U",
                            "units": ""
                        },
                        {
                            "$": "Weather Type",
                            "name": "W",
                            "units": ""
                        },
                        {
                            "$": "Precipitation Probability Day",
                            "name": "PPd",
                            "units": "%"
                        },
                        {
                            "$": "Precipitation Probability Night",
                            "name": "PPn",
                            "units": "%"
                        }
                    ]
                }
            }
        }

        report.parse_json(json)

        self.assertEquals(MetOfficeWeatherReport.FORECAST, report._data_type)
        self.assertEquals(metoffer.DAILY, report._time_period)
        self.assertIsNotNone(report._site_report)

class MetOfficeTests(unittest.TestCase):

    def setUp(self):
        self.license_keys = LicenseKeys()
        self.license_keys.load_license_key_file(os.path.dirname(__file__)+ os.sep + "test.keys")

        self.lat = 56.0720397
        self.lng = -3.1752001

    def test_init(self):
        met_office = MetOffice(self.license_keys)
        self.assertIsNotNone(met_office)

        self.assertIsNone(met_office.current_observation_response_file)
        self.assertIsNone(met_office.three_hourly_forecast_response_file)
        self.assertIsNone(met_office.daily_forecast_response_file)

        self.assertIsNotNone(met_office._met_office_api)

    def test_init_no_license_keys(self):
        with self.assertRaises(Exception):
            met_office = MetOffice(None)

    def test_observation(self):
        met_office = MetOffice(self.license_keys)
        self.assertIsNotNone(met_office)

        met_office.set_current_observation_response_file(os.path.dirname(__file__) +  os.sep + "observation.json")

        observation = met_office.current_observation(self.lat, self.lng)
        self.assertIsNotNone(observation)

        report = observation.get_latest_report()
        self.assertIsNotNone(report)

        date = DateFormatter.year_month_day(2017, 4, 3)
        report = observation.get_report_for_date(date)
        self.assertIsNotNone(report)

        datapoint = report.get_time_period_by_time("300")
        self.assertIsNotNone(datapoint)
        self.assertIsInstance(datapoint, ObservationDataPoint)

    def test_threehourly_forecast(self):
        met_office = MetOffice(self.license_keys)
        self.assertIsNotNone(met_office)

        met_office.set_three_hourly_forecast_response_file(os.path.dirname(__file__) +  os.sep + "forecast_3hourly.json")

        forecast = met_office.three_hourly_forecast(self.lat, self.lng)
        self.assertIsNotNone(forecast)

        report = forecast.get_latest_report()
        self.assertIsNotNone(report)

        date = DateFormatter.year_month_day(2017, 4, 3)
        report = forecast.get_report_for_date(date)
        self.assertIsNotNone(report)

        datapoint = report.get_time_period_by_time("540")
        self.assertIsNotNone(datapoint)
        self.assertIsInstance(datapoint, ThreeHourlyForecastDataPoint)

    def test_daily_forecast(self):
        met_office = MetOffice(self.license_keys)
        self.assertIsNotNone(met_office)

        met_office.set_daily_forecast_response_file(os.path.dirname(__file__) +  os.sep + "forecast_daily.json")

        forecast = met_office.daily_forecast(self.lat, self.lng)
        self.assertIsNotNone(forecast)

        report = forecast.get_latest_report()
        self.assertIsNotNone(report)

        date = DateFormatter.year_month_day(2017, 4, 3)
        report = forecast.get_report_for_date(date)
        self.assertIsNotNone(report)

        day_datapoint = report.get_time_period_by_type('Day')
        self.assertIsNotNone(day_datapoint)
        self.assertIsInstance(day_datapoint, DailyForecastDayDataPoint)

        night_datapoint = report.get_time_period_by_type('Night')
        self.assertIsNotNone(night_datapoint)
        self.assertIsInstance(night_datapoint, DailyForecastNightDataPoint)


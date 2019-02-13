import unittest
import os
import datetime
import json

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
from programy.utils.weather.metoffice import MetOffice24HourForecast, MetOffice5DayForecast, MetOfficeObservation, MetOfficeWeatherReport
from programy.utils.weather.metoffice import MetOffice
from programy.utils.license.keys import LicenseKeys
from programytest.client import TestClient


class DataPointTets(unittest.TestCase):

    def test_init(self):
        dp = DataPoint()
        self.assertIsNotNone(dp)

    def test_extract_attribute(self):
        dp = DataPoint()
        self.assertIsNotNone(dp)

        self.assertEqual("value", dp.extract_attribute({"item": "value"}, "item", MetOfficeWeatherReport.OBSERVATION))
        self.assertIsNone(dp.extract_attribute({"item": "value"}, "itemx", MetOfficeWeatherReport.OBSERVATION, None))

        self.assertEqual("value", dp.extract_attribute({"item": "value"}, "item", MetOfficeWeatherReport.FORECAST, metoffer.THREE_HOURLY))
        self.assertIsNone(dp.extract_attribute({"item": "value"}, "itemx", MetOfficeWeatherReport.FORECAST, metoffer.THREE_HOURLY))

        self.assertEqual("value", dp.extract_attribute({"item": "value"}, "item", MetOfficeWeatherReport.FORECAST,metoffer.DAILY))
        self.assertIsNone(dp.extract_attribute({"item": "value"}, "itemx", MetOfficeWeatherReport.FORECAST,metoffer.DAILY))

        self.assertIsNone(dp.extract_attribute({"item": "value"}, "itemx", 3))

    def test_direction_to_full_text(self):
        dp = DataPoint()
        self.assertIsNotNone(dp)

        self.assertEqual(dp.direction_to_full_text('N'), 'North')
        self.assertEqual(dp.direction_to_full_text('NNE'), 'North North East')
        self.assertEqual(dp.direction_to_full_text('NE'), 'North East')
        self.assertEqual(dp.direction_to_full_text('ENE'), 'East North East')
        self.assertEqual(dp.direction_to_full_text('E'), 'East')
        self.assertEqual(dp.direction_to_full_text('ESE'), 'East South East')
        self.assertEqual(dp.direction_to_full_text('SE'), 'South East')
        self.assertEqual(dp.direction_to_full_text('SSE'), 'South South East')
        self.assertEqual(dp.direction_to_full_text('S'), 'South')
        self.assertEqual(dp.direction_to_full_text('SSW'), 'South South West')
        self.assertEqual(dp.direction_to_full_text('SW'), 'South West')
        self.assertEqual(dp.direction_to_full_text('WSW'), 'West South West')
        self.assertEqual(dp.direction_to_full_text('W'), 'West')
        self.assertEqual(dp.direction_to_full_text('WNW'), 'West North West')
        self.assertEqual(dp.direction_to_full_text('NW'), 'North West')
        self.assertEqual(dp.direction_to_full_text('NNW'), 'North North West')

        self.assertEqual(dp.direction_to_full_text(''), "Unknown")
        self.assertEqual(dp.direction_to_full_text('other'), "Unknown")
        self.assertEqual(dp.direction_to_full_text(None), "Unknown")


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

        self.assertEqual("WEATHER TYPE Day WINDDIR S WINDSPEED 9 WINDGUST 16 TEMP 15 FEELS 13 HUMID 54 RAINPROB 0 UVINDEX 4 UVGUIDE Moderate exposure. Seek shade during midday hours, cover up and wear sunscreen VIS Very good - Between 20-40 km WEATHER Sunny day", dp.to_program_y_text())


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

        self.assertEqual("WEATHER Sunny day TEMP 4 FEELS 3 WINDDIR S WINDDIRFULL South WINDSPEED 2 VIS Moderate - Between 4-10 km UVINDEX 1 UVGUIDE Low exposure. No protection required. You can safely stay outside RAINPROB 0 HUMIDITY 96", dp.to_program_y_text())


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

        self.assertEqual("WEATHER Partly cloudy (day) TEMP 11 2 VISIBILITY V 35000 VF Very Good WIND D W DF West S 11 PRESSURE P 1021 PT R PTF Rising HUMIDITY 57 3", dp.to_program_y_text())

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

        self.assertEqual("Forecast", report._data_type)
        self.assertEqual("2017-04-03T09:00:00Z", report._time_period)

        self.assertIsNotNone(report._time_periods)
        self.assertEqual([], report._time_periods)

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


class DVTests(unittest.TestCase):

    def test_init(self):
        dv = DV(MetOfficeWeatherReport.FORECAST, metoffer.DAILY)
        self.assertIsNotNone(dv)

        self.assertEqual(MetOfficeWeatherReport.FORECAST, dv._data_type)
        self.assertEqual(metoffer.DAILY, dv._time_period)

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

        self.assertEqual(MetOfficeWeatherReport.FORECAST, report._data_type)
        self.assertEqual(metoffer.DAILY, report._time_period)

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

        self.assertEqual(MetOfficeWeatherReport.FORECAST, report._data_type)
        self.assertEqual(metoffer.DAILY, report._time_period)
        self.assertIsNotNone("", report._dv)


class MetOffice24HourForecastTests(unittest.TestCase):

    def test_parse_json(self):
        forecast = MetOffice24HourForecast()
        self.assertIsNotNone(forecast)

        json_data = { "SiteRep": { "DV": { "Location": { "Period": [ { "Rep": [ { "$": "360",
                                                              "D": "S",
                                                              "F": "3",
                                                              "G": "4",
                                                              "H": "96",
                                                              "Pp": "0",
                                                              "S": "2",
                                                              "T": "4",
                                                              "U": "1",
                                                              "V": "MO",
                                                              "W": "1"},
                                                            { "$": "540",
                                                              "D": "S",
                                                              "F": "11",
                                                              "G": "4",
                                                              "H": "77",
                                                              "Pp": "0",
                                                              "S": "2",
                                                              "T": "11",
                                                              "U": "2",
                                                              "V": "GO",
                                                              "W": "1"},
                                                            { "$": "720",
                                                              "D": "S",
                                                              "F": "13",
                                                              "G": "16",
                                                              "H": "54",
                                                              "Pp": "0",
                                                              "S": "9",
                                                              "T": "15",
                                                              "U": "4",
                                                              "V": "VG",
                                                              "W": "1"},
                                                            { "$": "900",
                                                              "D": "SSW",
                                                              "F": "13",
                                                              "G": "18",
                                                              "H": "55",
                                                              "Pp": "0",
                                                              "S": "11",
                                                              "T": "15",
                                                              "U": "2",
                                                              "V": "VG",
                                                              "W": "1"},
                                                            { "$": "1080",
                                                              "D": "SSW",
                                                              "F": "10",
                                                              "G": "16",
                                                              "H": "71",
                                                              "Pp": "1",
                                                              "S": "9",
                                                              "T": "12",
                                                              "U": "1",
                                                              "V": "GO",
                                                              "W": "3"},
                                                            { "$": "1260",
                                                              "D": "SSW",
                                                              "F": "7",
                                                              "G": "16",
                                                              "H": "84",
                                                              "Pp": "3",
                                                              "S": "7",
                                                              "T": "9",
                                                              "U": "0",
                                                              "V": "GO",
                                                              "W": "7"}],
                                                   "type": "Day",
                                                   "value": "2017-04-03Z"},
                                                 { "Rep": [ { "$": "0",
                                                              "D": "SSW",
                                                              "F": "7",
                                                              "G": "16",
                                                              "H": "86",
                                                              "Pp": "16",
                                                              "S": "7",
                                                              "T": "9",
                                                              "U": "0",
                                                              "V": "GO",
                                                              "W": "7"},
                                                            { "$": "180",
                                                              "D": "SSW",
                                                              "F": "8",
                                                              "G": "11",
                                                              "H": "92",
                                                              "Pp": "57",
                                                              "S": "4",
                                                              "T": "9",
                                                              "U": "0",
                                                              "V": "GO",
                                                              "W": "12"},
                                                            { "$": "360",
                                                              "D": "SW",
                                                              "F": "8",
                                                              "G": "9",
                                                              "H": "94",
                                                              "Pp": "56",
                                                              "S": "4",
                                                              "T": "9",
                                                              "U": "1",
                                                              "V": "GO",
                                                              "W": "12"},
                                                            { "$": "540",
                                                              "D": "NW",
                                                              "F": "10",
                                                              "G": "9",
                                                              "H": "91",
                                                              "Pp": "44",
                                                              "S": "4",
                                                              "T": "10",
                                                              "U": "1",
                                                              "V": "GO",
                                                              "W": "8"},
                                                            { "$": "720",
                                                              "D": "N",
                                                              "F": "11",
                                                              "G": "11",
                                                              "H": "82",
                                                              "Pp": "43",
                                                              "S": "7",
                                                              "T": "12",
                                                              "U": "2",
                                                              "V": "GO",
                                                              "W": "8"},
                                                            { "$": "900",
                                                              "D": "N",
                                                              "F": "11",
                                                              "G": "16",
                                                              "H": "79",
                                                              "Pp": "19",
                                                              "S": "9",
                                                              "T": "13",
                                                              "U": "1",
                                                              "V": "GO",
                                                              "W": "8"},
                                                            { "$": "1080",
                                                              "D": "N",
                                                              "F": "9",
                                                              "G": "20",
                                                              "H": "79",
                                                              "Pp": "14",
                                                              "S": "11",
                                                              "T": "11",
                                                              "U": "1",
                                                              "V": "VG",
                                                              "W": "8"},
                                                            { "$": "1260",
                                                              "D": "NNE",
                                                              "F": "8",
                                                              "G": "13",
                                                              "H": "73",
                                                              "Pp": "5",
                                                              "S": "7",
                                                              "T": "10",
                                                              "U": "0",
                                                              "V": "VG",
                                                              "W": "7"}],
                                                   "type": "Day",
                                                   "value": "2017-04-04Z"},
                                                 { "Rep": [ { "$": "0",
                                                              "D": "NNW",
                                                              "F": "6",
                                                              "G": "11",
                                                              "H": "81",
                                                              "Pp": "1",
                                                              "S": "4",
                                                              "T": "8",
                                                              "U": "0",
                                                              "V": "VG",
                                                              "W": "2"},
                                                            { "$": "180",
                                                              "D": "NW",
                                                              "F": "4",
                                                              "G": "11",
                                                              "H": "84",
                                                              "Pp": "1",
                                                              "S": "4",
                                                              "T": "6",
                                                              "U": "0",
                                                              "V": "GO",
                                                              "W": "0"},
                                                            { "$": "360",
                                                              "D": "NW",
                                                              "F": "4",
                                                              "G": "11",
                                                              "H": "82",
                                                              "Pp": "1",
                                                              "S": "4",
                                                              "T": "6",
                                                              "U": "1",
                                                              "V": "GO",
                                                              "W": "3"},
                                                            { "$": "540",
                                                              "D": "NW",
                                                              "F": "7",
                                                              "G": "18",
                                                              "H": "68",
                                                              "Pp": "4",
                                                              "S": "9",
                                                              "T": "9",
                                                              "U": "2",
                                                              "V": "VG",
                                                              "W": "7"},
                                                            { "$": "720",
                                                              "D": "NW",
                                                              "F": "9",
                                                              "G": "20",
                                                              "H": "59",
                                                              "Pp": "9",
                                                              "S": "11",
                                                              "T": "12",
                                                              "U": "3",
                                                              "V": "VG",
                                                              "W": "8"},
                                                            { "$": "900",
                                                              "D": "NW",
                                                              "F": "10",
                                                              "G": "22",
                                                              "H": "57",
                                                              "Pp": "9",
                                                              "S": "11",
                                                              "T": "12",
                                                              "U": "2",
                                                              "V": "VG",
                                                              "W": "8"},
                                                            { "$": "1080",
                                                              "D": "NNW",
                                                              "F": "9",
                                                              "G": "18",
                                                              "H": "62",
                                                              "Pp": "8",
                                                              "S": "9",
                                                              "T": "11",
                                                              "U": "1",
                                                              "V": "VG",
                                                              "W": "8"},
                                                            { "$": "1260",
                                                              "D": "NW",
                                                              "F": "8",
                                                              "G": "13",
                                                              "H": "70",
                                                              "Pp": "6",
                                                              "S": "7",
                                                              "T": "10",
                                                              "U": "0",
                                                              "V": "VG",
                                                              "W": "7"}],
                                                   "type": "Day",
                                                   "value": "2017-04-05Z"},
                                                 { "Rep": [ { "$": "0",
                                                              "D": "NNW",
                                                              "F": "7",
                                                              "G": "11",
                                                              "H": "79",
                                                              "Pp": "8",
                                                              "S": "7",
                                                              "T": "8",
                                                              "U": "0",
                                                              "V": "VG",
                                                              "W": "8"},
                                                            { "$": "180",
                                                              "D": "NW",
                                                              "F": "6",
                                                              "G": "9",
                                                              "H": "83",
                                                              "Pp": "5",
                                                              "S": "4",
                                                              "T": "7",
                                                              "U": "0",
                                                              "V": "VG",
                                                              "W": "7"},
                                                            { "$": "360",
                                                              "D": "WNW",
                                                              "F": "6",
                                                              "G": "7",
                                                              "H": "88",
                                                              "Pp": "3",
                                                              "S": "4",
                                                              "T": "7",
                                                              "U": "1",
                                                              "V": "VG",
                                                              "W": "3"},
                                                            { "$": "540",
                                                              "D": "NW",
                                                              "F": "9",
                                                              "G": "9",
                                                              "H": "77",
                                                              "Pp": "5",
                                                              "S": "4",
                                                              "T": "10",
                                                              "U": "2",
                                                              "V": "VG",
                                                              "W": "7"},
                                                            { "$": "720",
                                                              "D": "WNW",
                                                              "F": "12",
                                                              "G": "11",
                                                              "H": "61",
                                                              "Pp": "4",
                                                              "S": "4",
                                                              "T": "13",
                                                              "U": "4",
                                                              "V": "VG",
                                                              "W": "7"},
                                                            { "$": "900",
                                                              "D": "WNW",
                                                              "F": "13",
                                                              "G": "13",
                                                              "H": "58",
                                                              "Pp": "8",
                                                              "S": "7",
                                                              "T": "14",
                                                              "U": "2",
                                                              "V": "VG",
                                                              "W": "8"},
                                                            { "$": "1080",
                                                              "D": "WNW",
                                                              "F": "12",
                                                              "G": "9",
                                                              "H": "69",
                                                              "Pp": "5",
                                                              "S": "4",
                                                              "T": "12",
                                                              "U": "1",
                                                              "V": "VG",
                                                              "W": "7"},
                                                            { "$": "1260",
                                                              "D": "WNW",
                                                              "F": "9",
                                                              "G": "9",
                                                              "H": "77",
                                                              "Pp": "9",
                                                              "S": "4",
                                                              "T": "10",
                                                              "U": "0",
                                                              "V": "VG",
                                                              "W": "8"}],
                                                   "type": "Day",
                                                   "value": "2017-04-06Z"},
                                                 { "Rep": [ { "$": "0",
                                                              "D": "NW",
                                                              "F": "7",
                                                              "G": "9",
                                                              "H": "81",
                                                              "Pp": "9",
                                                              "S": "4",
                                                              "T": "9",
                                                              "U": "0",
                                                              "V": "VG",
                                                              "W": "8"},
                                                            { "$": "180",
                                                              "D": "WNW",
                                                              "F": "7",
                                                              "G": "9",
                                                              "H": "85",
                                                              "Pp": "7",
                                                              "S": "4",
                                                              "T": "8",
                                                              "U": "0",
                                                              "V": "VG",
                                                              "W": "7"},
                                                            { "$": "360",
                                                              "D": "WNW",
                                                              "F": "7",
                                                              "G": "7",
                                                              "H": "85",
                                                              "Pp": "10",
                                                              "S": "2",
                                                              "T": "8",
                                                              "U": "1",
                                                              "V": "VG",
                                                              "W": "8"},
                                                            { "$": "540",
                                                              "D": "WNW",
                                                              "F": "9",
                                                              "G": "9",
                                                              "H": "75",
                                                              "Pp": "11",
                                                              "S": "4",
                                                              "T": "10",
                                                              "U": "2",
                                                              "V": "VG",
                                                              "W": "8"},
                                                            { "$": "720",
                                                              "D": "WNW",
                                                              "F": "11",
                                                              "G": "11",
                                                              "H": "66",
                                                              "Pp": "9",
                                                              "S": "4",
                                                              "T": "12",
                                                              "U": "3",
                                                              "V": "VG",
                                                              "W": "8"},
                                                            { "$": "900",
                                                              "D": "WNW",
                                                              "F": "12",
                                                              "G": "11",
                                                              "H": "62",
                                                              "Pp": "9",
                                                              "S": "4",
                                                              "T": "13",
                                                              "U": "2",
                                                              "V": "VG",
                                                              "W": "8"},
                                                            { "$": "1080",
                                                              "D": "NW",
                                                              "F": "12",
                                                              "G": "7",
                                                              "H": "65",
                                                              "Pp": "8",
                                                              "S": "2",
                                                              "T": "12",
                                                              "U": "1",
                                                              "V": "VG",
                                                              "W": "8"},
                                                            { "$": "1260",
                                                              "D": "NW",
                                                              "F": "10",
                                                              "G": "7",
                                                              "H": "73",
                                                              "Pp": "8",
                                                              "S": "4",
                                                              "T": "10",
                                                              "U": "0",
                                                              "V": "VG",
                                                              "W": "8"}],
                                                   "type": "Day",
                                                   "value": "2017-04-07Z"}],
                                     "continent": "EUROPE",
                                     "country": "ENGLAND",
                                     "elevation": "4.0",
                                     "i": "351747",
                                     "lat": "51.4007",
                                     "lon": "-0.3337",
                                     "name": "HAMPTON COURT PALACE"},
                       "dataDate": "2017-04-03T09:00:00Z",
                       "type": "Forecast"},
               "Wx": { "Param": [ { "$": "Feels Like Temperature",
                                    "name": "F",
                                    "units": "C"},
                                  { "$": "Wind Gust",
                                    "name": "G",
                                    "units": "mph"},
                                  { "$": "Screen Relative Humidity",
                                    "name": "H",
                                    "units": "%"},
                                  { "$": "Temperature",
                                    "name": "T",
                                    "units": "C"},
                                  {"$": "Visibility", "name": "V", "units": ""},
                                  { "$": "Wind Direction",
                                    "name": "D",
                                    "units": "compass"},
                                  { "$": "Wind Speed",
                                    "name": "S",
                                    "units": "mph"},
                                  { "$": "Max UV Index",
                                    "name": "U",
                                    "units": ""},
                                  { "$": "Weather Type",
                                    "name": "W",
                                    "units": ""},
                                  { "$": "Precipitation Probability",
                                    "name": "Pp",
                                    "units": "%"}]}}}

        forecast.parse_json(json_data)


class MetOffice5DayForecastTests(unittest.TestCase):

    def test_parse_json(self):
        forecast = MetOffice5DayForecast()
        self.assertIsNotNone(forecast)

        json_data = {"SiteRep": {
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


        forecast.parse_json(json_data)


class MetOfficeObservationTests(unittest.TestCase):

    def test_parse_json(self):
        observation = MetOfficeObservation()
        self.assertIsNotNone(observation)

        json_data = { "SiteRep": {
                        "DV": {
                            "Location": {
                                "Period": [
                                    {
                                        "Rep": [
                                            {
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
                                            },
                                            {
                                                "$": "720",
                                                "D": "WSW",
                                                "Dp": "2.2",
                                                "H": "51.6",
                                                "P": "1021",
                                                "Pt": "R",
                                                "S": "9",
                                                "T": "11.7",
                                                "V": "35000",
                                                "W": "1"
                                            },
                                            {
                                                "$": "780",
                                                "D": "WSW",
                                                "Dp": "2.6",
                                                "H": "50.7",
                                                "P": "1021",
                                                "Pt": "F",
                                                "S": "10",
                                                "T": "12.4",
                                                "V": "35000",
                                                "W": "1"
                                            },
                                            {
                                                "$": "840",
                                                "D": "W",
                                                "Dp": "2.9",
                                                "H": "49.4",
                                                "P": "1020",
                                                "Pt": "F",
                                                "S": "14",
                                                "T": "13.1",
                                                "V": "35000",
                                                "W": "1"
                                            },
                                            {
                                                "$": "900",
                                                "D": "WSW",
                                                "Dp": "3.7",
                                                "H": "50.3",
                                                "P": "1020",
                                                "Pt": "F",
                                                "S": "9",
                                                "T": "13.7",
                                                "V": "35000",
                                                "W": "3"
                                            },
                                            {
                                                "$": "960",
                                                "D": "W",
                                                "Dp": "3.8",
                                                "H": "51.0",
                                                "P": "1020",
                                                "Pt": "F",
                                                "S": "13",
                                                "T": "13.6",
                                                "V": "35000",
                                                "W": "1"
                                            },
                                            {
                                                "$": "1020",
                                                "D": "WSW",
                                                "Dp": "3.4",
                                                "H": "52.6",
                                                "P": "1021",
                                                "Pt": "R",
                                                "S": "11",
                                                "T": "12.7",
                                                "V": "35000",
                                                "W": "1"
                                            },
                                            {
                                                "$": "1080",
                                                "D": "WSW",
                                                "Dp": "3.3",
                                                "H": "56.2",
                                                "P": "1021",
                                                "Pt": "R",
                                                "S": "9",
                                                "T": "11.6",
                                                "V": "35000",
                                                "W": "1"
                                            },
                                            {
                                                "$": "1140",
                                                "D": "WSW",
                                                "Dp": "3.1",
                                                "H": "63.9",
                                                "P": "1022",
                                                "Pt": "R",
                                                "S": "3",
                                                "T": "9.5",
                                                "V": "30000",
                                                "W": "0"
                                            },
                                            {
                                                "$": "1200",
                                                "D": "SSW",
                                                "Dp": "3.2",
                                                "H": "70.8",
                                                "P": "1022",
                                                "Pt": "R",
                                                "S": "6",
                                                "T": "8.1",
                                                "V": "29000",
                                                "W": "0"
                                            },
                                            {
                                                "$": "1260",
                                                "D": "SSW",
                                                "Dp": "2.8",
                                                "H": "73.7",
                                                "P": "1022",
                                                "Pt": "R",
                                                "S": "6",
                                                "T": "7.1",
                                                "V": "29000",
                                                "W": "0"
                                            },
                                            {
                                                "$": "1320",
                                                "D": "SSW",
                                                "Dp": "2.2",
                                                "H": "69.6",
                                                "P": "1022",
                                                "Pt": "R",
                                                "S": "8",
                                                "T": "7.3",
                                                "V": "30000",
                                                "W": "0"
                                            },
                                            {
                                                "$": "1380",
                                                "D": "SSW",
                                                "Dp": "2.4",
                                                "H": "71.7",
                                                "P": "1022",
                                                "Pt": "F",
                                                "S": "10",
                                                "T": "7.1",
                                                "V": "29000",
                                                "W": "0"
                                            }
                                        ],
                                        "type": "Day",
                                        "value": "2017-04-02Z"
                                    },
                                    {
                                        "Rep": [
                                            {
                                                "$": "0",
                                                "D": "SSW",
                                                "Dp": "2.5",
                                                "H": "73.2",
                                                "P": "1021",
                                                "Pt": "F",
                                                "S": "9",
                                                "T": "6.9",
                                                "V": "29000",
                                                "W": "0"
                                            },
                                            {
                                                "$": "60",
                                                "D": "SW",
                                                "Dp": "2.4",
                                                "H": "74.7",
                                                "P": "1021",
                                                "Pt": "F",
                                                "S": "7",
                                                "T": "6.5",
                                                "V": "30000",
                                                "W": "0"
                                            },
                                            {
                                                "$": "120",
                                                "D": "SW",
                                                "Dp": "3.0",
                                                "H": "76.0",
                                                "P": "1020",
                                                "Pt": "F",
                                                "S": "8",
                                                "T": "6.9",
                                                "V": "30000",
                                                "W": "0"
                                            },
                                            {
                                                "$": "180",
                                                "D": "WSW",
                                                "Dp": "1.9",
                                                "H": "71.1",
                                                "P": "1020",
                                                "Pt": "F",
                                                "S": "6",
                                                "T": "6.7",
                                                "V": "30000",
                                                "W": "0"
                                            },
                                            {
                                                "$": "240",
                                                "D": "WSW",
                                                "Dp": "2.0",
                                                "H": "79.5",
                                                "P": "1020",
                                                "Pt": "F",
                                                "S": "5",
                                                "T": "5.2",
                                                "V": "30000",
                                                "W": "0"
                                            },
                                            {
                                                "$": "300",
                                                "D": "SW",
                                                "Dp": "2.1",
                                                "G": "19",
                                                "H": "73.2",
                                                "P": "1019",
                                                "Pt": "F",
                                                "S": "8",
                                                "T": "6.5",
                                                "V": "30000",
                                                "W": "0"
                                            },
                                            {
                                                "$": "360",
                                                "D": "WNW",
                                                "Dp": "1.8",
                                                "H": "79.5",
                                                "P": "1019",
                                                "Pt": "F",
                                                "S": "2",
                                                "T": "5.0",
                                                "V": "30000",
                                                "W": "1"
                                            },
                                            {
                                                "$": "420",
                                                "D": "NNW",
                                                "Dp": "2.5",
                                                "H": "80.7",
                                                "P": "1019",
                                                "Pt": "F",
                                                "S": "1",
                                                "T": "5.5",
                                                "V": "30000",
                                                "W": "1"
                                            },
                                            {
                                                "$": "480",
                                                "D": "SSW",
                                                "Dp": "3.0",
                                                "H": "65.2",
                                                "P": "1018",
                                                "Pt": "F",
                                                "S": "7",
                                                "T": "9.1",
                                                "V": "35000",
                                                "W": "1"
                                            },
                                            {
                                                "$": "540",
                                                "D": "SW",
                                                "Dp": "3.6",
                                                "H": "62.3",
                                                "P": "1018",
                                                "Pt": "F",
                                                "S": "15",
                                                "T": "10.4",
                                                "V": "35000",
                                                "W": "7"
                                            },
                                            {
                                                "$": "600",
                                                "D": "SW",
                                                "Dp": "3.9",
                                                "H": "61.6",
                                                "P": "1018",
                                                "Pt": "F",
                                                "S": "15",
                                                "T": "10.9",
                                                "V": "35000",
                                                "W": "7"
                                            },
                                            {
                                                "$": "660",
                                                "D": "SW",
                                                "Dp": "4.2",
                                                "H": "57.3",
                                                "P": "1017",
                                                "Pt": "F",
                                                "S": "10",
                                                "T": "12.3",
                                                "V": "35000",
                                                "W": "3"
                                            }
                                        ],
                                        "type": "Day",
                                        "value": "2017-04-03Z"
                                    }
                                ],
                                "continent": "EUROPE",
                                "country": "SCOTLAND",
                                "elevation": "57.0",
                                "i": "3166",
                                "lat": "55.928",
                                "lon": "-3.343",
                                "name": "EDINBURGH/GOGARBANK"
                            },
                            "dataDate": "2017-04-03T11:00:00Z",
                            "type": "Obs"
                        },
                        "Wx": {
                            "Param": [
                                {
                                    "$": "Wind Gust",
                                    "name": "G",
                                    "units": "mph"
                                },
                                {
                                    "$": "Temperature",
                                    "name": "T",
                                    "units": "C"
                                },
                                {
                                    "$": "Visibility",
                                    "name": "V",
                                    "units": "m"
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
                                    "$": "Weather Type",
                                    "name": "W",
                                    "units": ""
                                },
                                {
                                    "$": "Pressure",
                                    "name": "P",
                                    "units": "hpa"
                                },
                                {
                                    "$": "Pressure Tendency",
                                    "name": "Pt",
                                    "units": "Pa/s"
                                },
                                {
                                    "$": "Dew Point",
                                    "name": "Dp",
                                    "units": "C"
                                },
                                {
                                    "$": "Screen Relative Humidity",
                                    "name": "H",
                                    "units": "%"
                                }
                            ]
                        }
                    }
                }

        observation.parse_json(json_data)


class MockMetOffice(MetOffice):

    def __init__(self, license_keys):
        MetOffice.__init__(self)
        self._observation_file = None
        self._forecast_file = None

    def get_forecast_data(self, lat, lon, forecast_type):
        with open(self._forecast_file) as json_forecast_file:
            return json.load(json_forecast_file)

    def get_observation_data(self, lat, lon):
        with open(self._observation_file) as json_observation_file:
            return json.load(json_observation_file)


class MetOfficeTests(unittest.TestCase):

    def setUp(self):
        self._client = TestClient()
        self._client.add_license_keys_store()

        self.lat = 56.0720397
        self.lng = -3.1752001

    def test_init(self):
        met_office = MetOffice()
        self.assertIsNotNone(met_office)

    def test_init_no_license_keys(self):
        with self.assertRaises(Exception):
            met_office = MetOffice(None)

    def test_observation(self):
        met_office = MockMetOffice(self._client.license_keys)
        self.assertIsNotNone(met_office)
        met_office._observation_file = os.path.dirname(__file__) +  os.sep + "observation.json"
        self.assertTrue(os.path.exists(met_office._observation_file))

        observation = met_office.current_observation(self.lat, self.lng)
        self.assertIsNotNone(observation)

    def tes_five_day_forecast(self):
        met_office = MockMetOffice(self._client.license_keys)
        self.assertIsNotNone(met_office)
        met_office._forecast_file = os.path.dirname(__file__) +  os.sep + "forecast_3hourly.json"
        self.assertTrue(os.path.exists(met_office._forecast_file))

        forecast = met_office.five_day_forecast(self.lat, self.lng)
        self.assertIsNotNone(forecast)

    def tets_twentyfour_hour_forecast(self):
        met_office = MockMetOffice(self._client.license_keys)
        self.assertIsNotNone(met_office)
        met_office._forecast_file = os.path.dirname(__file__) +  os.sep + "forecast_daily.json"
        self.assertTrue(os.path.exists(met_office._forecast_file))

        forecast = met_office.twentyfour_hour_forecast(self.lat, self.lng)
        self.assertIsNotNone(forecast)


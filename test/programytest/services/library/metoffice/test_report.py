import datetime
import unittest
import metoffer
from programy.services.library.metoffice.metoffice import MetOfficeWeatherReport
from programy.services.library.metoffice.metoffice import Report


class ReportTests(unittest.TestCase):

    def test_init(self):
        report = Report("Forecast", "2017-04-03T09:00:00Z")
        self.assertIsNotNone(report)

        self.assertEqual("Forecast", report._data_type)
        self.assertEqual("2017-04-03T09:00:00Z", report.time_period)

        self.assertIsNotNone(report.time_periods)
        self.assertEqual([], report.time_periods)

        self.assertIsNone(report.type)
        self.assertIsNone(report.report_date)

    def test_parse_json_daily(self):
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

        self.assertEqual(2, len(report.time_periods))

        self.assertEqual(report.type, "Day")
        self.assertEqual(report.report_date, datetime.datetime(2017, 4, 3, 0, 0))

        last = report.get_last_time_period()
        self.assertIsNotNone(last)

        period = report.get_time_period_by_type("Day")
        self.assertIsNotNone(period)

        period = report.get_time_period_by_type("Other")
        self.assertIsNone(period)

    def test_parse_json_daily_not_day_or_night(self):
        report = Report(MetOfficeWeatherReport.FORECAST, metoffer.DAILY)
        self.assertIsNotNone(report)

        json = { "Rep": [ { "$": "XXXX",
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
                        { "$": "YYY",
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
        with self.assertRaises(ValueError):
            report.parse_json(json)

    def test_parse_json_3hourly(self):
        report = Report(MetOfficeWeatherReport.FORECAST, metoffer.THREE_HOURLY)
        self.assertIsNotNone(report)

        json =  {"Rep": [{"$": "360",
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
                             {"$": "540",
                              "D": "S",
                              "F": "11",
                              "G": "4",
                              "H": "77",
                              "Pp": "0",
                              "S": "2",
                              "T": "11",
                              "U": "2",
                              "V": "GO",
                              "W": "1"}],
               "type": "Day",
               "value": "2017-04-03Z"}
        report.parse_json(json)

        time = report.get_time_period_by_time("360")
        self.assertIsNotNone(time)

        time = report.get_time_period_by_time("999")
        self.assertIsNone(time)

    def test_parse_json_3hourly_no_timeperiods(self):
        report = Report(MetOfficeWeatherReport.FORECAST, metoffer.THREE_HOURLY)
        self.assertIsNotNone(report)

        json =  {"Rep": [],
                 "type": "Day",
                 "value": "2017-04-03Z"}
        report.parse_json(json)

        time = report.get_time_period_by_time("360")
        self.assertIsNone(time)

        self.assertIsNone(report.get_last_time_period())
        self.assertIsNone(report.get_time_period_by_type('Day'))
        self.assertIsNone(report.get_time_period_by_time('360'))

    def test_parse_json_3hourly_no_value(self):
        report = Report(MetOfficeWeatherReport.FORECAST, metoffer.THREE_HOURLY)
        self.assertIsNotNone(report)

        json =  {"Rep": [],
                 "value": "2017-04-03Z"}
        with self.assertRaises(ValueError):
            report.parse_json(json)

    def test_parse_json_3hourly_wrong_value(self):
        report = Report(MetOfficeWeatherReport.FORECAST, metoffer.THREE_HOURLY)
        self.assertIsNotNone(report)

        json =  {"Rep": [],
                 "type": "Day",
                 "value": "XXXXXXX"}
        with self.assertRaises(ValueError):
            report.parse_json(json)

    def test_parse_json_unknown_datatype(self):
        report = Report(999, metoffer.DAILY)
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
        with self.assertRaises(ValueError):
            report.parse_json(json)

    def test_parse_json_unknown_time_period(self):
        report = Report(MetOfficeWeatherReport.FORECAST, "Weekly")
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
        with self.assertRaises(ValueError):
            report.parse_json(json)

    def test_parse_json_missing_type(self):
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
               "value": "2017-04-03Z"}
        with self.assertRaises(ValueError):
            report.parse_json(json)

    def test_parse_json_missing_value(self):
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
               "type": "Day"}
        with self.assertRaises(ValueError):
            report.parse_json(json)

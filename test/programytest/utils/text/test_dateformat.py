import unittest
import datetime

from programy.utils.text.dateformat import DateFormatter

from programytest.custom import CustomAssertions

#############################################################################
#

class TextUtilsTests(unittest.TestCase, CustomAssertions):

    DEFAULT_DATETIME_REGEX = "^.{3}\s*.{3}\s*\d{1,}\s\d{2}:\d{2}:\d{2}\s\d{4}"

    def test_year_month_day(self):
        result = DateFormatter.year_month_day(2017, 7, 7)
        self.assertIsNotNone(result)
        self.assertEqual(datetime.datetime(2017, 7, 7, 0, 0), result)

    def test_year_month_day_now(self):
        result = DateFormatter.year_month_day_now()
        self.assertIsNotNone(result)
        now = datetime.datetime.now()
        self.assertEqual(datetime.datetime(now.year, now.month, now.day, 0, 0), result)

    def test_init_basic(self):
        df = DateFormatter()
        self.assertIsNotNone(df)
        now = datetime.datetime.now()
        self.assertEqual(now.year, df.time_now.year)
        self.assertEqual(now.month, df.time_now.month)
        self.assertEqual(now.day, df.time_now.day)
        self.assertEqual(now.hour, df.time_now.hour)
        self.assertEqual(now.minute, df.time_now.minute)
        self.assertEqual(now.second, df.time_now.second)

    def test_init_weeks(self):
        df = DateFormatter(weeks=1)
        self.assertIsNotNone(df)
        now = datetime.datetime.now() + datetime.timedelta(days=7)
        self.assertEqual(now.year, df.time_now.year)
        self.assertEqual(now.month, df.time_now.month)
        self.assertEqual(now.day, df.time_now.day)
        self.assertEqual(now.hour, df.time_now.hour)
        self.assertEqual(now.minute, df.time_now.minute)
        self.assertEqual(now.second, df.time_now.second)

    def test_init_days(self):
        df = DateFormatter(days=1)
        self.assertIsNotNone(df)
        now = datetime.datetime.now() + datetime.timedelta(days=1)
        self.assertEqual(now.year, df.time_now.year)
        self.assertEqual(now.month, df.time_now.month)
        self.assertEqual(now.day, df.time_now.day)
        self.assertEqual(now.hour, df.time_now.hour)
        self.assertEqual(now.minute, df.time_now.minute)
        self.assertEqual(now.second, df.time_now.second)

    def test_init_days(self):
        df = DateFormatter(hours=1)
        self.assertIsNotNone(df)
        now = datetime.datetime.now() + datetime.timedelta(hours=1)
        self.assertEqual(now.year, df.time_now.year)
        self.assertEqual(now.month, df.time_now.month)
        self.assertEqual(now.day, df.time_now.day)
        self.assertEqual(now.hour, df.time_now.hour)
        self.assertEqual(now.minute, df.time_now.minute)
        self.assertEqual(now.second, df.time_now.second)

    def test_init_minutes(self):
        df = DateFormatter(minutes=1)
        self.assertIsNotNone(df)
        now = datetime.datetime.now() + datetime.timedelta(minutes=1)
        self.assertEqual(now.year, df.time_now.year)
        self.assertEqual(now.month, df.time_now.month)
        self.assertEqual(now.day, df.time_now.day)
        self.assertEqual(now.hour, df.time_now.hour)
        self.assertEqual(now.minute, df.time_now.minute)
        self.assertEqual(now.second, df.time_now.second)

    def test_init_seconds(self):
        df = DateFormatter(seconds=1)
        self.assertIsNotNone(df)
        now = datetime.datetime.now() + datetime.timedelta(seconds=1)
        self.assertEqual(now.year, df.time_now.year)
        self.assertEqual(now.month, df.time_now.month)
        self.assertEqual(now.day, df.time_now.day)
        self.assertEqual(now.hour, df.time_now.hour)
        self.assertEqual(now.minute, df.time_now.minute)
        self.assertEqual(now.second, df.time_now.second)

    def test_init_all(self):
        df = DateFormatter(weeks=1, days=1, hours=1, minutes=1, seconds=1)
        self.assertIsNotNone(df)
        now = datetime.datetime.now() + datetime.timedelta(days=8, hours=1, minutes=1, seconds=1)
        self.assertEqual(now.year, df.time_now.year)
        self.assertEqual(now.month, df.time_now.month)
        self.assertEqual(now.day, df.time_now.day)
        self.assertEqual(now.hour, df.time_now.hour)
        self.assertEqual(now.minute, df.time_now.minute)
        self.assertEqual(now.second, df.time_now.second)

    def test_abbreviated_weekday(self):
        df = DateFormatter()
        self.assertIsNotNone(df)
        result = df.abbreviated_weekday()
        self.assertIsNotNone(result)
        self.assertRegex(result, r"[Mon|Tue|Wed|Thu|Fri|Sat|Sun]")

    def test_full_weekday(self):
        df = DateFormatter()
        self.assertIsNotNone(df)
        result = df.full_weekday()
        self.assertIsNotNone(result)
        self.assertRegex(result, r"[Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday]")

    def test_abbreviated_month(self):
        df = DateFormatter()
        self.assertIsNotNone(df)
        result = df.abbreviated_month()
        self.assertIsNotNone(result)
        self.assertRegex(result, r"[Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec]")

    def test_full_month(self):
        df = DateFormatter()
        self.assertIsNotNone(df)
        result = df.full_month()
        self.assertIsNotNone(result)
        self.assertRegex(result, r"[January|February|March|April|May|June|July|August|September|October|November|December]")

    def test_locate_appropriate_date_time(self):
        df = DateFormatter()
        self.assertIsNotNone(df)
        result = df.locate_appropriate_date_time()
        self.assertIsNotNone(result)
        self.assertRegex(result, TextUtilsTests.DEFAULT_DATETIME_REGEX)

    def test_decimal_day_of_month(self):
        df = DateFormatter()
        self.assertIsNotNone(df)
        result = df.decimal_day_of_month()
        self.assertIsNotNone(result)
        self.assertRegex(result, "\d{1}|\d{2}")

    def test_hour_24_hour_clock(self):
        df = DateFormatter()
        self.assertIsNotNone(df)
        result = df.hour_12_hour_clock()
        self.assertIsNotNone(result)
        self.assertRegex(result, "\d{1}|\d{2}")

    def test_hour_12_hour_clock(self):
        df = DateFormatter()
        self.assertIsNotNone(df)
        result = df.hour_12_hour_clock()
        self.assertIsNotNone(result)
        self.assertRegex(result, "\d{1}|\d{2}")

    def test_decimal_day_of_year(self):
        df = DateFormatter()
        self.assertIsNotNone(df)
        result = df.decimal_day_of_year()
        self.assertIsNotNone(result)
        self.assertRegex(result, "\d{1}|\d{2}")

    def test_decimal_month(self):
        df = DateFormatter()
        self.assertIsNotNone(df)
        result = df.decimal_month()
        self.assertIsNotNone(result)
        self.assertRegex(result, "\d{1}|\d{2}")

    def test_decimal_minute(self):
        df = DateFormatter()
        self.assertIsNotNone(df)
        result = df.decimal_minute()
        self.assertIsNotNone(result)
        self.assertRegex(result, "\d{1}|\d{2}")

    def test_decimal_second(self):
        df = DateFormatter()
        self.assertIsNotNone(df)
        result = df.decimal_second()
        self.assertIsNotNone(result)
        self.assertRegex(result, r"\d{1}|\d{2}")

    def test_decimal_week_number_sunday_as_first(self):
        df = DateFormatter()
        self.assertIsNotNone(df)
        result = df.decimal_week_number_monday_as_first()
        self.assertIsNotNone(result)
        self.assertRegex(result, "\d{1}|\d{2}")

    def test_decimal_week_number_monday_as_first(self):
        df = DateFormatter()
        self.assertIsNotNone(df)
        result = df.decimal_week_number_monday_as_first()
        self.assertIsNotNone(result)
        self.assertRegex(result, "\d{1}|\d{2}")

    def test_decimal_weekday(self):
        df = DateFormatter()
        self.assertIsNotNone(df)
        result = df.decimal_weekday()
        self.assertIsNotNone(result)
        self.assertRegex(result, "\d{1}|\d{2}")

    def test_am_or_pm(self):
        df = DateFormatter()
        self.assertIsNotNone(df)
        result = df.am_or_pm()
        self.assertIsNotNone(result)
        self.assertRegex(r"[AM|PM]", result)

    def test_date_representation(self):
        df = DateFormatter()
        self.assertIsNotNone(df)
        result = df.date_representation()
        self.assertIsNotNone(result)
        self.assertRegex(result, r"\d{2}/\d{2}/\d{2}")

    def test_time_representation(self):
        df = DateFormatter()
        self.assertIsNotNone(df)
        result = df.time_representation()
        self.assertIsNotNone(result)
        self.assertRegex(result, r"\d{2}:\d{2}:\d{2}")

    def test_year_2_digit(self):
        df = DateFormatter()
        self.assertIsNotNone(df)
        result = df.year_2_digit()
        self.assertIsNotNone(result)
        self.assertRegex(result, r"\d{2}")

    def test_year_4_digit(self):
        df = DateFormatter()
        self.assertIsNotNone(df)
        result = df.year_4_digit()
        self.assertIsNotNone(result)
        self.assertRegex(result, r"\d{4}")

    def test_timezone_name(self):
        df = DateFormatter()
        self.assertIsNotNone(df)
        result = df.timezone_name()
        self.assertIsNotNone(result)
        self.assertEqual("", result)

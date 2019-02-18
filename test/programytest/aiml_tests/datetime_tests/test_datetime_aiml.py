import unittest
import os

from programy.utils.text.dateformat import DateFormatter

from programytest.client import TestClient

class DateTimeAIMLTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(DateTimeAIMLTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])
        self.add_sets_store([os.path.dirname(__file__)+ os.sep + "sets"])
        self.add_maps_store([os.path.dirname(__file__)+ os.sep + "maps"])


class DateTimeAIMLTests(unittest.TestCase):

    DEFAULT_DATETIME_REGEX = "^.*.{3}\s*.{3}\s*\d{1,}\s\d{2}:\d{2}:\d{2}\s\d{4}"

    def setUp(self):
        client = DateTimeAIMLTestClient()
        self._client_context = client.create_client_context("testid")

        self._client_context.brain.dynamics.add_dynamic_set('number', "programy.dynamic.sets.numeric.IsNumeric", None)
        self.date = DateFormatter()

    def test_season(self):
        response = self._client_context.bot.ask_question(self._client_context, "SEASON")
        self.assertIsNotNone(response)
        self.assertRegex(response, "[Winter|Spring|Summer|Autumn|Fall]")

    def test_day(self):
        response = self._client_context.bot.ask_question(self._client_context, "DAY")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Today is %s."%(self.date.full_weekday()))

    def test_tomorrow(self):
        response = self._client_context.bot.ask_question(self._client_context, "TOMORROW")
        self.assertIsNotNone(response)
        self.date = DateFormatter(days=1)
        self.assertEqual(response, self.date.full_weekday()+".")

    def test_year(self):
        response = self._client_context.bot.ask_question(self._client_context, "YEAR")
        self.assertIsNotNone(response)
        self.assertEqual(response, "This is %s."%(self.date.year_4_digit()))

        response = self._client_context.bot.ask_question(self._client_context, "YEAR NEXT")
        self.assertIsNotNone(response)
        self.assertEqual(response, "This is %s."%(self.date.year_4_digit()))

    def test_next_year(self):
        next_year = (int(self.date.year_4_digit()))+1

        response = self._client_context.bot.ask_question(self._client_context, "NEXT YEAR")
        self.assertIsNotNone(response)
        self.assertEqual(response, "%d."%(next_year))

        response = self._client_context.bot.ask_question(self._client_context, "NEXT YEAR NEXT")
        self.assertIsNotNone(response)
        self.assertEqual(response, "%d."%(next_year))

    def test_last_year(self):
        last_year = (int(self.date.year_4_digit()))-1

        response = self._client_context.bot.ask_question(self._client_context, "LAST YEAR")
        self.assertIsNotNone(response)
        self.assertEqual(response, "%d."%(last_year))

        response = self._client_context.bot.ask_question(self._client_context, "LAST YEAR AGO")
        self.assertIsNotNone(response)
        self.assertEqual(response, "%d."%(last_year))

    def test_month(self):
        response = self._client_context.bot.ask_question(self._client_context, "MONTH")
        self.assertIsNotNone(response)
        self.assertEqual(response, "This is %s."%(self.date.full_month()))

    def test_time(self):
        response = self._client_context.bot.ask_question(self._client_context, "TIME")
        self.assertIsNotNone(response)

        hour = self.date.hour_12_hour_clock()
        min = self.date.decimal_minute()
        ampm = self.date.am_or_pm()
        self.assertRegex(response, "The time is %s:%s %s."%(hour, min, ampm))

    def test_day_phase(self):
        response = self._client_context.bot.ask_question(self._client_context,  "DAY PHASE")
        self.assertIsNotNone(response)
        self.assertRegex(response, "[Noon|Afternoon|Night]")

    def test_days_until_day(self):
        response = self._client_context.bot.ask_question(self._client_context, "DAYS UNTIL THURSDAY")
        self.assertIsNotNone(response)
        self.assertRegex(response, "\d{1}|\d{2}")

    def test_days_until_christmas(self):
        response = self._client_context.bot.ask_question(self._client_context, "DAYS UNTIL CHRISTMAS")
        self.assertIsNotNone(response)
        self.assertRegex(response, "\d{1}|\d{2}")

    def test_days_until_day_month_year(self):
        response = self._client_context.bot.ask_question(self._client_context, "DAYS UNTIL APRIL 01 2017")
        self.assertIsNotNone(response)
        self.assertRegex(response, "\d{1}|\d{2}")

    def test_days_until_month_year(self):
        response = self._client_context.bot.ask_question(self._client_context, "DAYS UNTIL APRIL 01")
        self.assertIsNotNone(response)
        self.assertRegex(response, "\d{1}|\d{2}")

    def test_date(self):
        response = self._client_context.bot.ask_question(self._client_context,  "DATE")
        self.assertIsNotNone(response)
        self.assertRegex(response, "Today is .* \\d{2}, \\d{4}")

    def test_date_tomorrow(self):
        response = self._client_context.bot.ask_question(self._client_context, "DATE TOMORROW")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

    def test_date_and_time(self):
        response = self._client_context.bot.ask_question(self._client_context, "DATE AND TIME")
        self.assertIsNotNone(response)
        self.assertRegex(response, "The date and time is .{3} .{3}\s*\\d{1}|\\d{2} \\d{2}:\\d{2}:\\d{2} \\d{4}")

    def test_tomorrowdate_month_day_year(self):
        response = self._client_context.bot.ask_question(self._client_context,  "TOMORROWDATE APRIL 01 2017")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

    def test_tomorrowdate_month_end_carry_over(self):
        response = self._client_context.bot.ask_question(self._client_context,  "TOMORROWDATE JANUARY 31 2017")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

        response = self._client_context.bot.ask_question(self._client_context,  "TOMORROWDATE FEBRUARY 28 2012")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

        response = self._client_context.bot.ask_question(self._client_context,  "TOMORROWDATE FEBRUARY 28 2016")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

        response = self._client_context.bot.ask_question(self._client_context,  "TOMORROWDATE FEBRUARY 28 2020")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

        response = self._client_context.bot.ask_question(self._client_context,  "TOMORROWDATE FEBRUARY 28 2024")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

        response = self._client_context.bot.ask_question(self._client_context,  "TOMORROWDATE FEBRUARY 28 2028")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

        response = self._client_context.bot.ask_question(self._client_context,  "TOMORROWDATE FEBRUARY 28 2019")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

        response = self._client_context.bot.ask_question(self._client_context,  "TOMORROWDATE FEBRUARY 29 2020")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

        response = self._client_context.bot.ask_question(self._client_context,  "TOMORROWDATE MATCH 30 2020")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

        response = self._client_context.bot.ask_question(self._client_context,  "TOMORROWDATE APRIL 31 2020")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

        response = self._client_context.bot.ask_question(self._client_context,  "TOMORROWDATE MAY 31 2020")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

        response = self._client_context.bot.ask_question(self._client_context,  "TOMORROWDATE JUNE 30 2020")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

        response = self._client_context.bot.ask_question(self._client_context,  "TOMORROWDATE JULY 31 2020")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

        response = self._client_context.bot.ask_question(self._client_context,  "TOMORROWDATE AUGUST 31 2020")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

        response = self._client_context.bot.ask_question(self._client_context,  "TOMORROWDATE SEPTEMBER 30 2020")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

        response = self._client_context.bot.ask_question(self._client_context,  "TOMORROWDATE OCTOBER 31 2020")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

        response = self._client_context.bot.ask_question(self._client_context,  "TOMORROWDATE NOVEBER 30 2020")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

        response = self._client_context.bot.ask_question(self._client_context,  "TOMORROWDATE DECEMBER 31 2020")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

    def test_date_in_one_days(self):
        response = self._client_context.bot.ask_question(self._client_context,  "DATE IN 1 DAYS")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

    def test_date_in_two_days(self):
        response = self._client_context.bot.ask_question(self._client_context, "DATE IN 2 DAYS")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

    def test_date_in_ten_days(self):
        response = self._client_context.bot.ask_question(self._client_context, "DATE IN 10 DAYS")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

    def test_day_after_tomorrow_date(self):
        response = self._client_context.bot.ask_question(self._client_context, "DAYAFTERTOMORROWDATE")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

    def test_day_after_tomorrow_date_specific(self):
        response = self._client_context.bot.ask_question(self._client_context, "DAYAFTERTOMORROWDATE APRIL 01 2017")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

    def test_day_after_tomorrow(self):
        response = self._client_context.bot.ask_question(self._client_context, "DAY AFTER TOMORROW")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".*")

    def test_days_until_weekday(self):
        response = self._client_context.bot.ask_question(self._client_context, "DAYS UNTIL THURSDAY")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".*")

    def test_date_on(self):
        response = self._client_context.bot.ask_question(self._client_context, "DATE ON THURSDAY")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".*")

    def test_date_weekend(self):
        response = self._client_context.bot.ask_question(self._client_context, "DATE ON WEEKEND")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".*")

    def test_weekday_in_five_days(self):
        response = self._client_context.bot.ask_question(self._client_context, "WEEKDAY IN 5 DAYS")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".*")

    def test_date_a_week_from(self):
        response = self._client_context.bot.ask_question(self._client_context, "DATE A WEEK FROM THURSDAY")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".*")



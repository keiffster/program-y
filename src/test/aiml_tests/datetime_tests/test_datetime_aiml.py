import unittest
import os

from programy.config.brain import BrainFileConfiguration
from programy.utils.text.dateformat import DateFormatter

from test.aiml_tests.client import TestClient

unittest.util._MAX_LENGTH=2000

class BasicTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(BasicTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration(files=os.path.dirname(__file__))
        self.configuration.brain_configuration._set_files = BrainFileConfiguration(files=os.path.dirname(__file__)+"/sets", extension=".txt")
        self.configuration.brain_configuration._map_files = BrainFileConfiguration(files=os.path.dirname(__file__)+"/maps", extension=".txt")


class DateTimeAIMLTests(unittest.TestCase):

    DEFAULT_DATETIME_REGEX = "^.*.{3}\s*.{3}\s*\d{1,}\s\d{2}:\d{2}:\d{2}\s\d{4}"

    def setUp(self):
        DateTimeAIMLTests.test_client = BasicTestClient()
        self.date = DateFormatter()

    def test_season(self):
        response = DateTimeAIMLTests.test_client.bot.ask_question("test", "SEASON")
        self.assertIsNotNone(response)
        self.assertRegex(response, "[Winter|Spring|Summer|Autumn]")

    def test_day(self):
        response = DateTimeAIMLTests.test_client.bot.ask_question("test", "DAY")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Today is %s"%(self.date.full_weekday()))

    def test_tomorrow(self):
        response = DateTimeAIMLTests.test_client.bot.ask_question("test", "TOMORROW")
        self.assertIsNotNone(response)
        self.date = DateFormatter(days=1)
        self.assertEqual(response, self.date.full_weekday())

    def test_year(self):
        response = DateTimeAIMLTests.test_client.bot.ask_question("test", "YEAR")
        self.assertIsNotNone(response)
        self.assertEqual(response, "This is %s"%(self.date.year_4_digit()))

        response = DateTimeAIMLTests.test_client.bot.ask_question("test", "YEAR NEXT")
        self.assertIsNotNone(response)
        self.assertEqual(response, "This is %s"%(self.date.year_4_digit()))

    def test_next_year(self):
        next_year = (int(self.date.year_4_digit()))+1

        response = DateTimeAIMLTests.test_client.bot.ask_question("test", "NEXT YEAR")
        self.assertIsNotNone(response)
        self.assertEqual(response, "%d"%(next_year))

        response = DateTimeAIMLTests.test_client.bot.ask_question("test", "NEXT YEAR NEXT")
        self.assertIsNotNone(response)
        self.assertEqual(response, "%d"%(next_year))

    def test_last_year(self):
        last_year = (int(self.date.year_4_digit()))-1

        response = DateTimeAIMLTests.test_client.bot.ask_question("test", "LAST YEAR")
        self.assertIsNotNone(response)
        self.assertEqual(response, "%d"%(last_year))

        response = DateTimeAIMLTests.test_client.bot.ask_question("test", "LAST YEAR AGO")
        self.assertIsNotNone(response)
        self.assertEqual(response, "%d"%(last_year))

    def test_month(self):
        response = DateTimeAIMLTests.test_client.bot.ask_question("test", "MONTH")
        self.assertIsNotNone(response)
        self.assertEqual(response, "This is %s"%(self.date.full_month()))

    def test_time(self):
        response = DateTimeAIMLTests.test_client.bot.ask_question("test", "TIME")
        self.assertIsNotNone(response)

        hour = self.date.hour_12_hour_clock()
        min = self.date.decimal_minute()
        ampm = self.date.am_or_pm()
        self.assertRegex(response, "The time is %s:%s %s"%(hour, min, ampm))

    def test_day_phase(self):
        response = DateTimeAIMLTests.test_client.bot.ask_question("test",  "DAY PHASE")
        self.assertIsNotNone(response)
        self.assertRegex(response, "[Noon|Afternoon|Night]")

    def test_days_until_day(self):
        response = DateTimeAIMLTests.test_client.bot.ask_question("test", "DAYS UNTIL THURSDAY")
        self.assertIsNotNone(response)
        self.assertRegex(response, "\d{1}|\d{2}")

    def test_days_until_christmas(self):
        response = DateTimeAIMLTests.test_client.bot.ask_question("test", "DAYS UNTIL CHRISTMAS")
        self.assertIsNotNone(response)
        self.assertRegex(response, "\d{1}|\d{2}")

    def test_days_until_day_month_year(self):
        response = DateTimeAIMLTests.test_client.bot.ask_question("test", "DAYS UNTIL APRIL 01 2017")
        self.assertIsNotNone(response)
        self.assertRegex(response, "\d{1}|\d{2}")

    def test_days_until_month_year(self):
        response = DateTimeAIMLTests.test_client.bot.ask_question("test", "DAYS UNTIL APRIL 01")
        self.assertIsNotNone(response)
        self.assertRegex(response, "\d{1}|\d{2}")

    def test_date(self):
        response = DateTimeAIMLTests.test_client.bot.ask_question("test",  "DATE")
        self.assertIsNotNone(response)
        self.assertRegex(response, "Today is .* \\d{2}, \\d{4}")

    def test_date_tomorrow(self):
        response = DateTimeAIMLTests.test_client.bot.ask_question("test", "DATE TOMORROW")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

    def test_date_and_time(self):
        response = DateTimeAIMLTests.test_client.bot.ask_question("test", "DATE AND TIME")
        self.assertIsNotNone(response)
        self.assertRegex(response, "The date and time is .{3} .{3}\s*\\d{1}|\\d{2} \\d{2}:\\d{2}:\\d{2} \\d{4}")

    def test_tomorrowdate_month_day_year(self):
        response = DateTimeAIMLTests.test_client.bot.ask_question("test",  "TOMORROWDATE APRIL 01 2017")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

    def test_tomorrowdate_month_end_carry_over(self):
        response = DateTimeAIMLTests.test_client.bot.ask_question("test",  "TOMORROWDATE JANUARY 31 2017")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

        response = DateTimeAIMLTests.test_client.bot.ask_question("test",  "TOMORROWDATE FEBRUARY 28 2012")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

        response = DateTimeAIMLTests.test_client.bot.ask_question("test",  "TOMORROWDATE FEBRUARY 28 2016")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

        response = DateTimeAIMLTests.test_client.bot.ask_question("test",  "TOMORROWDATE FEBRUARY 28 2020")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

        response = DateTimeAIMLTests.test_client.bot.ask_question("test",  "TOMORROWDATE FEBRUARY 28 2024")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

        response = DateTimeAIMLTests.test_client.bot.ask_question("test",  "TOMORROWDATE FEBRUARY 28 2028")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

        response = DateTimeAIMLTests.test_client.bot.ask_question("test",  "TOMORROWDATE FEBRUARY 28 2019")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

        response = DateTimeAIMLTests.test_client.bot.ask_question("test",  "TOMORROWDATE FEBRUARY 29 2020")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

        response = DateTimeAIMLTests.test_client.bot.ask_question("test",  "TOMORROWDATE MATCH 30 2020")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

        response = DateTimeAIMLTests.test_client.bot.ask_question("test",  "TOMORROWDATE APRIL 31 2020")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

        response = DateTimeAIMLTests.test_client.bot.ask_question("test",  "TOMORROWDATE MAY 31 2020")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

        response = DateTimeAIMLTests.test_client.bot.ask_question("test",  "TOMORROWDATE JUNE 30 2020")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

        response = DateTimeAIMLTests.test_client.bot.ask_question("test",  "TOMORROWDATE JULY 31 2020")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

        response = DateTimeAIMLTests.test_client.bot.ask_question("test",  "TOMORROWDATE AUGUST 31 2020")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

        response = DateTimeAIMLTests.test_client.bot.ask_question("test",  "TOMORROWDATE SEPTEMBER 30 2020")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

        response = DateTimeAIMLTests.test_client.bot.ask_question("test",  "TOMORROWDATE OCTOBER 31 2020")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

        response = DateTimeAIMLTests.test_client.bot.ask_question("test",  "TOMORROWDATE NOVEBER 30 2020")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

        response = DateTimeAIMLTests.test_client.bot.ask_question("test",  "TOMORROWDATE DECEMBER 31 2020")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

    def test_date_in_one_days(self):
        response = DateTimeAIMLTests.test_client.bot.ask_question("test",  "DATE IN 1 DAYS")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

    def test_date_in_two_days(self):
        response = DateTimeAIMLTests.test_client.bot.ask_question("test", "DATE IN 2 DAYS")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

    def test_date_in_ten_days(self):
        response = DateTimeAIMLTests.test_client.bot.ask_question("test", "DATE IN 10 DAYS")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

    def test_day_after_tomorrow_date(self):
        response = DateTimeAIMLTests.test_client.bot.ask_question("test", "DAYAFTERTOMORROWDATE")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

    def test_day_after_tomorrow_date_specific(self):
        response = DateTimeAIMLTests.test_client.bot.ask_question("test", "DAYAFTERTOMORROWDATE APRIL 01 2017")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".* \\d{1}|\\d{2} \\d{4}")

    def test_day_after_tomorrow(self):
        response = DateTimeAIMLTests.test_client.bot.ask_question("test", "DAY AFTER TOMORROW")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".*")

    def test_days_until_weekday(self):
        response = DateTimeAIMLTests.test_client.bot.ask_question("test", "DAYS UNTIL THURSDAY")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".*")

    def test_date_on(self):
        response = DateTimeAIMLTests.test_client.bot.ask_question("test", "DATE ON THURSDAY")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".*")

    def test_date_weekend(self):
        response = DateTimeAIMLTests.test_client.bot.ask_question("test", "DATE ON WEEKEND")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".*")

    def test_weekday_in_five_days(self):
        response = DateTimeAIMLTests.test_client.bot.ask_question("test", "WEEKDAY IN 5 DAYS")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".*")

    def test_date_a_week_from(self):
        response = DateTimeAIMLTests.test_client.bot.ask_question("test", "DATE A WEEK FROM THURSDAY")
        self.assertIsNotNone(response)
        self.assertRegex(response, ".*")



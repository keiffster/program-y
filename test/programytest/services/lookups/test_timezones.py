import unittest
from programy.services.lookups.timezones import Timezones


class TimezonesTests(unittest.TestCase):

    def test_codes(self):
        self.assertEqual(["GMT", "Greenwich Mean Time", "UTC±00"], Timezones.CODES["GMT"])

    def test_timezones(self):
        self.assertEqual(["GMT", "Greenwich Mean Time", "UTC±00"], Timezones.TIMEZONES["Greenwich Mean Time"])

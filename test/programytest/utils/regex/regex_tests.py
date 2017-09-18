import unittest
import re

class RegularExpressionTests(unittest.TestCase):

    def test_anything(self):
        pattern = re.compile(r"^.*$", re.IGNORECASE)
        self.assertIsNotNone(pattern.match(""))
        self.assertIsNotNone(pattern.match("This"))
        self.assertIsNotNone(pattern.match("This That"))

    def test_anytext(self):
        pattern = re.compile(r"^.+$", re.IGNORECASE)
        self.assertIsNone(pattern.match(""))
        self.assertIsNotNone(pattern.match("This"))
        self.assertIsNotNone(pattern.match("This That"))

    def test_anyinteger(self):
        pattern = re.compile(r"^\d+$", re.IGNORECASE)
        self.assertIsNone(pattern.match(""))
        self.assertIsNotNone(pattern.match("123"))

    def test_anydecimal(self):
        pattern = re.compile(r"^\d+\.\d+$", re.IGNORECASE)
        self.assertIsNotNone(pattern.match("123.3"))

    def test_anynumber(self):
        pattern = re.compile(r"^[\d+\.\d+$]|[\d+]$", re.IGNORECASE)
        self.assertIsNotNone(pattern.match(".23"))
        self.assertIsNotNone(pattern.match("123"))
        self.assertIsNotNone(pattern.match("123.3"))

    def test_legion(self):
        pattern = re.compile(r"^LEGION$", re.IGNORECASE)
        self.assertIsNotNone(pattern.match("LEGION"))
        self.assertIsNotNone(pattern.match("legion"))
        self.assertIsNotNone(pattern.match("LegioN"))
        self.assertIsNone(pattern.match("LEGIONAIRRE"))

    def test_email(self):
        pattern = re.compile(r"^[-a-z0-9_.]+@(?:[-a-z0-9]+\.)+[a-z]{2,6}$", re.IGNORECASE)
        self.assertIsNotNone(pattern.match("keith@keithsterling.com"))

    def test_postcode(self):
        pattern = re.compile(r"^[a-z]{1,2}\d{1,2}[a-z]?\s*\d[a-z]{2}$", re.IGNORECASE)
        self.assertIsNotNone(pattern.match("KY1 1YY"))

    def test_zipcode(self):
        pattern = re.compile(r"^\d{5}(?:[-\s]\d{4})?$", re.IGNORECASE)
        self.assertIsNotNone(pattern.match("12345"))
        self.assertIsNotNone(pattern.match("12345 1234"))

    def test_ukdate(self):
        pattern = re.compile(r"^[0123]?\d[-/\s\.](?:[01]\d|[a-z]{3,})[-/\s\.](?:\d{2})?\d{2}$", re.IGNORECASE)
        self.assertIsNotNone(pattern.match("31-02-2017"))

    def test_time(self):
        pattern = re.compile(r"^\d{1,2}:\d{1,2}(?:\s*[aApP]\.?[mM]\.?)?$", re.IGNORECASE)
        self.assertIsNotNone(pattern.match("11:23am"))


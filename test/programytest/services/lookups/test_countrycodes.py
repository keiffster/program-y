import unittest
from programy.services.lookups.countrycodes import CountryCodes


class CountryCodesTests(unittest.TestCase):

    def test_names(self):
        self.assertEqual(['Ukraine', 'UA', 'UKR', '804'], CountryCodes.NAMES['Ukraine'])

    def test_two_digits(self):
        self.assertEqual(['Ukraine', 'UA', 'UKR', '804'], CountryCodes.TWO_DIGITS['UA'])

    def test_three_digits(self):
        self.assertEqual(['Ukraine', 'UA', 'UKR', '804'], CountryCodes.THREE_DIGITS['UKR'])

    def test_numeric(self):
        self.assertEqual(['Ukraine', 'UA', 'UKR', '804'], CountryCodes.NUMERIC['804'])

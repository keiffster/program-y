import unittest

from programy.dynamic.maps.roman import MapDecimalToRoman
from programy.dynamic.maps.roman import MapRomanToDecimal


class IsRomanNumeralDynamicSetTests(unittest.TestCase):

    def test_romantodec(self):
        dyn_map = MapRomanToDecimal(None)
        self.assertIsNotNone(dyn_map)
        self.assertEquals("20", dyn_map.map_value(None, "testid", "XX"))
        self.assertEquals("4", dyn_map.map_value(None, "testid", "IV"))

    def test_dectoroman(self):
        dyn_map = MapDecimalToRoman(None)
        self.assertIsNotNone(dyn_map)
        self.assertEquals("XX", dyn_map.map_value(None, "testid", "20"))
        self.assertEquals("IV", dyn_map.map_value(None, "testid", "4"))

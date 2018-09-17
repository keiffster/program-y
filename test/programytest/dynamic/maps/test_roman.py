import unittest

from programy.dynamic.maps.roman import MapDecimalToRoman
from programy.dynamic.maps.roman import MapRomanToDecimal
from programy.context import ClientContext

from programytest.client import TestClient


class IsRomanNumeralDynamicSetTests(unittest.TestCase):

    def setUp(self):
        self._client_context = ClientContext(TestClient(), "testid")

    def test_romantodec(self):
        dyn_map = MapRomanToDecimal(None)
        self.assertIsNotNone(dyn_map)
        self.assertEqual("20", dyn_map.map_value(self._client_context, "XX"))
        self.assertEqual("4", dyn_map.map_value(self._client_context, "IV"))

    def test_dectoroman(self):
        dyn_map = MapDecimalToRoman(None)
        self.assertIsNotNone(dyn_map)
        self.assertEqual("XX", dyn_map.map_value(self._client_context, "20"))
        self.assertEqual("IV", dyn_map.map_value(self._client_context, "4"))

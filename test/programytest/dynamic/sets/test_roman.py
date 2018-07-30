import unittest

from programy.dynamic.sets.roman import IsRomanNumeral
from programy.context import ClientContext

from programytest.client import TestClient


class IsRomanNumeralDynamicSetTests(unittest.TestCase):

    def setUp(self):
        self._client_context = ClientContext(TestClient(), "testid")

    def test_isromannumeral(self):
        dyn_var = IsRomanNumeral(None)
        self.assertIsNotNone(dyn_var)
        self.assertTrue(dyn_var.is_member(self._client_context, "XXVI"))
        self.assertFalse(dyn_var.is_member(self._client_context, "12345"))
        self.assertFalse(dyn_var.is_member(self._client_context, "VIVE"))
        self.assertFalse(dyn_var.is_member(self._client_context, None))

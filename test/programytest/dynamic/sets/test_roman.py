import unittest

from programy.dynamic.sets.roman import IsRomanNumeral


class IsRomanNumeralDynamicSetTests(unittest.TestCase):

    def test_isromannumeral(self):
        dyn_var = IsRomanNumeral(None)
        self.assertIsNotNone(dyn_var)
        self.assertTrue(dyn_var.is_member(None, "testid", "XXVI"))
        self.assertFalse(dyn_var.is_member(None, "testid", "12345"))
        self.assertFalse(dyn_var.is_member(None, "testid", "VIVE"))
        self.assertFalse(dyn_var.is_member(None, "testid", None))

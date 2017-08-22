import unittest

from programy.dynamic.sets.numeric import IsNumeric

class IsNumericDynamicSetTests(unittest.TestCase):

    def test_isnumeric(self):
        dyn_var = IsNumeric(None)
        self.assertIsNotNone(dyn_var)
        self.assertTrue(dyn_var.is_member(None, "testid", "12345"))
        self.assertFalse(dyn_var.is_member(None, "testid", "ABCDEF"))
        self.assertFalse(dyn_var.is_member(None, "testid", None))

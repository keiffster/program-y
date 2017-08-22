import unittest

from programy.dynamic.variables.datetime import GetTime

class GetTimeDynamicVarTests(unittest.TestCase):

    def test_gettime(self):
        dyn_var = GetTime(None)
        self.assertIsNotNone(dyn_var)
        time = dyn_var.get_value(None, "testid")
        self.assertIsNotNone(time)


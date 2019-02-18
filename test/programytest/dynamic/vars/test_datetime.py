import unittest

from programy.dynamic.variables.datetime import GetTime
from programy.context import ClientContext

from programytest.client import TestClient

class GetTimeDynamicVarTests(unittest.TestCase):

    def setUp(self):
        self._client_context = ClientContext(TestClient(), "testid")

    def test_gettime(self):
        dyn_var = GetTime(None)
        self.assertIsNotNone(dyn_var)
        time = dyn_var.get_value(self._client_context)
        self.assertIsNotNone(time)


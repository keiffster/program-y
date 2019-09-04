import unittest

from programy.dynamic.maps.successor import SuccessorMap
from programy.context import ClientContext

from programytest.client import TestClient


class TestSingularMaps(unittest.TestCase):

    def setUp(self):
        self._client_context = ClientContext(TestClient(), "testid")

    def test_successor(self):
        map = SuccessorMap(None)
        self.assertEqual("2", map.map_value(self._client_context, "1"))

    def test_successor_text(self):
        map = SuccessorMap(None)
        self.assertEqual("", map.map_value(self._client_context, "one"))


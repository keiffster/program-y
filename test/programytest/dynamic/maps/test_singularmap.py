import unittest

from programy.dynamic.maps.singular import SingularMap
from programy.context import ClientContext

from programytest.client import TestClient


class TestSingularMaps(unittest.TestCase):

    def setUp(self):
        self._client_context = ClientContext(TestClient(), "testid")

    def test_static_map(self):
        map = SingularMap(None)
        self.assertEqual("MOUSE", map.map_value(self._client_context, "MICE"))

    def test_plural_ies_to_singular(self):
        map = SingularMap(None)
        self.assertEqual("HOLLY", map.map_value(self._client_context, "HOLLIES"))

    def test_plural_s_to_singular(self):
        map = SingularMap(None)
        self.assertEqual("CURL", map.map_value(self._client_context, "CURLS"))

    def test_plural_no_match(self):
        map = SingularMap(None)
        self.assertEqual("FISH", map.map_value(self._client_context, "FISH"))

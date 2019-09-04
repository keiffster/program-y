import unittest

from programy.dynamic.maps.stemmer import StemmerMap
from programy.context import ClientContext

from programytest.client import TestClient


class TestStemmerMaps(unittest.TestCase):

    def setUp(self):
        self._client_context = ClientContext(TestClient(), "testid")

    def test_static_map(self):
        map = StemmerMap(None)
        self.assertEqual("troubl", map.map_value(self._client_context, "trouble"))
        self.assertEqual("troubl", map.map_value(self._client_context, "troubles"))
        self.assertEqual("troubl", map.map_value(self._client_context, "troubled"))
        self.assertEqual("troubl", map.map_value(self._client_context, "troubling"))
        self.assertEqual("", map.map_value(self._client_context, ""))

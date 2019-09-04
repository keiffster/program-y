import unittest

from programy.dynamic.maps.lemmatize import LemmatizeMap
from programy.context import ClientContext

from programytest.client import TestClient


class TestLemmatizeMaps(unittest.TestCase):

    def setUp(self):
        self._client_context = ClientContext(TestClient(), "testid")

    def test_static_map(self):
        map = LemmatizeMap(None)
        self.assertEqual("octopus", map.map_value(self._client_context, "octopi"))
        self.assertEqual("sheep", map.map_value(self._client_context, "sheep"))
        self.assertEqual("fish", map.map_value(self._client_context, "fish"))
        self.assertEqual("mouse", map.map_value(self._client_context, "mice"))
        self.assertEqual("holly", map.map_value(self._client_context, "hollies"))

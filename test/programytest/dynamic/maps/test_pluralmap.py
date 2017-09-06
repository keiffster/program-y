import unittest

from programy.dynamic.maps.plural import PluralMap

class TestPluralMaps(unittest.TestCase):

    def test_static_map(self):
        map = PluralMap(None)
        self.assertEqual("MICE", map.map_value(None, "clientid", "MOUSE"))

    def test_singular_y_to_plural(self):
        map = PluralMap(None)
        self.assertEqual("HOLLIES", map.map_value(None, "clientid", "HOLLY"))

    def test_singular_s_to_plural(self):
        map = PluralMap(None)
        self.assertEqual("COWS", map.map_value(None, "clientid", "COW"))

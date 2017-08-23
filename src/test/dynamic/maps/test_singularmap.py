import unittest

from programy.dynamic.maps.singular import SingularMap

class TestSingularMaps(unittest.TestCase):

    def test_static_map(self):
        map = SingularMap(None)
        self.assertEqual("MOUSE", map.map_value(None, "clientid", "MICE"))

    def test_plural_ies_to_singular(self):
        map = SingularMap(None)
        self.assertEqual("HOLLY", map.map_value(None, "clientid", "HOLLIES"))

    def test_plural_s_to_singular(self):
        map = SingularMap(None)
        self.assertEqual("CURL", map.map_value(None, "clientid", "CURLS"))

    def test_plural_no_match(self):
        map = SingularMap(None)
        self.assertEqual("FISH", map.map_value(None, "clientid", "FISH"))

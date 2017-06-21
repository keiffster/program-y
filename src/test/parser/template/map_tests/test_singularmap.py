import unittest

from programy.parser.template.maps.singular import SingularMap

class TestSingularMaps(unittest.TestCase):

    def test_static_map(self):
        map = SingularMap()
        self.assertEqual("MOUSE", map.map("MICE"))

    def test_plural_ies_to_singular(self):
        map = SingularMap()
        self.assertEqual("HOLLY", map.map("HOLLIES"))

    def test_plural_s_to_singular(self):
        map = SingularMap()
        self.assertEqual("CURL", map.map("CURLS"))


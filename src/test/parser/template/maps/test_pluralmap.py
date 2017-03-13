import unittest

from programy.parser.template.maps.plural import PluralMap

class TestPluralMaps(unittest.TestCase):

    def test_static_map(self):
        map = PluralMap()
        self.assertEqual("MICE", map.map("MOUSE"))

    def test_singular_y_to_plural(self):
        map = PluralMap()
        self.assertEqual("HOLLIES", map.map("HOLLY"))

    def test_singular_s_to_plural(self):
        map = PluralMap()
        self.assertEqual("COWS", map.map("COW"))

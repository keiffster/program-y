import unittest

from programy.parser.template.maps.predecessor import PredecessorMap

class TestSingularMaps(unittest.TestCase):

    def test_successor(self):
        map = PredecessorMap()
        self.assertEqual("1", map.map("2"))



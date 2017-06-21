import unittest

from programy.parser.template.maps.predecessor import PredecessorMap

class TestPredecessorMaps(unittest.TestCase):

    def test_predecessor(self):
        map = PredecessorMap()
        self.assertEqual("1", map.map("2"))

    def test_predecessor_text(self):
        map = PredecessorMap()
        self.assertEqual("", map.map("two"))


import unittest

from programy.dynamic.maps.predecessor import PredecessorMap

class TestPredecessorMaps(unittest.TestCase):

    def test_predecessor(self):
        map = PredecessorMap(None)
        self.assertEqual("1", map.map_value(None, "clientid", "2"))

    def test_predecessor_text(self):
        map = PredecessorMap(None)
        self.assertEqual("", map.map_value(None, "clientid", "two"))


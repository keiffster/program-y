import unittest

from programy.dynamic.maps.successor import SuccessorMap

class TestSingularMaps(unittest.TestCase):

    def test_successor(self):
        map = SuccessorMap(None)
        self.assertEqual("2", map.map_value(None, "clientid", "1"))

    def test_successor_text(self):
        map = SuccessorMap(None)
        self.assertEqual("", map.map_value(None, "clientid", "one"))


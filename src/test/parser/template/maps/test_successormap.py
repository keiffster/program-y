import unittest

from programy.parser.template.maps.successor import SuccessorMap

class TestSingularMaps(unittest.TestCase):

    def test_successor(self):
        map = SuccessorMap()
        self.assertEqual("2", map.map("1"))



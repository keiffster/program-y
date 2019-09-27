import unittest

from programy.dynamic.maps.map import DynamicMap
from programy.config.brain.brain import BrainDynamicsConfiguration


class MockDynamicMap(DynamicMap):

    def __init__(self, config):
        DynamicMap.__init__(self, config)

    def map_value(self, client_context, input_value):
        raise NotImplementedError()


class DynamicMapTests(unittest.TestCase):

    def test_init(self):
        config = BrainDynamicsConfiguration()
        map = MockDynamicMap(config)
        self.assertIsNotNone(map)
        self.assertIsNotNone(map.config)
        self.assertEqual(config, map.config)

        with self.assertRaises(Exception):
            map.map_value(None, None, None)
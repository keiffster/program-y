import unittest

from programy.dynamic.sets.set import DynamicSet
from programy.config.brain.brain import BrainDynamicsConfiguration


class MockDynamicSet(DynamicSet):

    def __init__(self, config):
        DynamicSet.__init__(self, config)

    def is_member(self, client_context, value, additional=None):
        raise NotImplementedError()


class DynamicSetTests(unittest.TestCase):

    def test_init(self):
        config = BrainDynamicsConfiguration()
        set = MockDynamicSet(config)
        self.assertIsNotNone(set)
        self.assertIsNotNone(set.config)
        self.assertEqual(config, set.config)

        with self.assertRaises(Exception):
            set.is_member(None, None, None)
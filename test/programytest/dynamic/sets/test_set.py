import unittest

from programy.dynamic.sets.set import DynamicSet
from programy.config.brain.brain import BrainDynamicsConfiguration


class DynamicSetTests(unittest.TestCase):

    def test_init(self):
        config = BrainDynamicsConfiguration()
        set = DynamicSet(config)
        self.assertIsNotNone(set)
        self.assertIsNotNone(set.config)
        self.assertEqual(config, set.config)

        with self.assertRaises(Exception):
            set.is_member(None, None, None)
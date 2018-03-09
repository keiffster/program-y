import unittest

from programy.dynamic.variables.variable import DynamicVariable
from programy.config.brain.brain import BrainDynamicsConfiguration


class DynamicVariableTests(unittest.TestCase):

    def test_init(self):
        config = BrainDynamicsConfiguration()
        var = DynamicVariable(config)
        self.assertIsNotNone(var)
        self.assertIsNotNone(var.config)
        self.assertEqual(config, var.config)

        with self.assertRaises(Exception):
            var.get_value(None, None, None)
import unittest

from programy.config.brain.brain import BrainDynamicsConfiguration
from programy.dynamic.variables.variable import DynamicVariable


class MockDynamicVariable(DynamicVariable):

    def __init__(self, config):
        DynamicVariable.__init__(self, config)

    def get_value(self, client_context, value):
        raise NotImplementedError()


class DynamicVariableTests(unittest.TestCase):

    def test_init(self):
        config = BrainDynamicsConfiguration()
        var = MockDynamicVariable(config)
        self.assertIsNotNone(var)
        self.assertIsNotNone(var.config)
        self.assertEqual(config, var.config)

        with self.assertRaises(Exception):
            var.get_value(None, None, None)
import unittest

from programy.clients.events.console.config import ConsoleConfiguration
from programy.config.brain.dynamic import BrainDynamicsConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.dynamic.dynamics import DynamicsCollection
from programy.dynamic.sets.numeric import IsNumeric
from programy.dynamic.maps.plural import PluralMap
from programy.dynamic.maps.singular import SingularMap
from programy.dynamic.maps.predecessor import PredecessorMap
from programy.dynamic.maps.successor import SuccessorMap
from programy.dynamic.variables.variable import DynamicSettableVariable


class MockDynamicsCollection(DynamicsCollection):

    def __init__(self):
        DynamicsCollection.__init__(self)

    def _set_value(self, client_context, name, value):
        raise Exception("Mock Exception")


class MockDynamicSettableVariable(DynamicSettableVariable):

    def __init__(self, config, value=None, set_exception=False):
        DynamicSettableVariable.__init__(self, config)
        self._value = value
        self._set_exception = set_exception

    def get_value(self, client_context, value):
        return self._value

    def set_value(self, client_context, value):
        if self._set_exception is True:
            raise Exception("Mock Exception")
        self._value = value


class DynamicsCollectionTests(unittest.TestCase):

    def test_init(self):
        collection = DynamicsCollection()
        self.assertIsNotNone(collection)
        self.assertIsNotNone(collection.dynamic_sets)
        self.assertIsNotNone(collection.dynamic_maps)
        self.assertIsNotNone(collection.dynamic_vars)

    def test_load_from_configuration_no_data(self):
        collection = DynamicsCollection()
        self.assertIsNotNone(collection)

        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            dynamic:
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        dynamics_config = BrainDynamicsConfiguration()
        dynamics_config.load_config_section(yaml, brain_config, ".")

        collection.load_from_configuration(dynamics_config)

        self.assertIsNotNone(collection.dynamic_sets)
        self.assertTrue(collection.is_dynamic_set("NUMBER"))

        self.assertIsNotNone(collection.dynamic_maps)
        self.assertTrue(collection.is_dynamic_map("PLURAL"))
        self.assertTrue(collection.is_dynamic_map("SINGULAR"))
        self.assertTrue(collection.is_dynamic_map("PREDECESSOR"))
        self.assertTrue(collection.is_dynamic_map("SUCCESSOR"))

        self.assertIsNotNone(collection.dynamic_vars)

    def test_load_from_configuration_no_config(self):
        collection = DynamicsCollection()
        self.assertIsNotNone(collection)
        collection.load_from_configuration(None)

        self.assertEquals({}, collection.dynamic_sets)
        self.assertEquals({}, collection.dynamic_maps)
        self.assertEquals({}, collection.dynamic_vars)

    def test_load_from_configuration(self):
        collection = DynamicsCollection()
        self.assertIsNotNone(collection)

        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            dynamic:
                variables:
                    gettime: programy.dynamic.variables.datetime.GetTime
                sets:
                    roman: programy.dynamic.sets.roman.IsRomanNumeral
                maps:
                    romantodec: programy.dynamic.maps.roman.MapRomanToDecimal
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        dynamics_config = BrainDynamicsConfiguration()
        dynamics_config.load_config_section(yaml, brain_config, ".")

        collection.load_from_configuration(dynamics_config)

        self.assertIsNotNone(collection.dynamic_sets)
        self.assertTrue(collection.is_dynamic_set("ROMAN"))
        self.assertTrue(collection.is_dynamic_set("NUMBER"))

        self.assertIsNotNone(collection.dynamic_maps)
        self.assertTrue(collection.is_dynamic_map("ROMANTODEC"))
        self.assertTrue(collection.is_dynamic_map("PLURAL"))
        self.assertTrue(collection.is_dynamic_map("SINGULAR"))
        self.assertTrue(collection.is_dynamic_map("PREDECESSOR"))
        self.assertTrue(collection.is_dynamic_map("SUCCESSOR"))

        self.assertIsNotNone(collection.dynamic_vars)
        self.assertTrue(collection.is_dynamic_var("GETTIME"))

    def test_load_default_dynamic_sets(self):
        dynamics_config = BrainDynamicsConfiguration()

        collection = DynamicsCollection()
        collection.load_default_dynamic_sets(dynamics_config)

        self.assertEquals(1, len(collection.dynamic_sets))
        self.assertTrue(IsNumeric.NAME in collection.dynamic_sets)

        self.assertIsNone(collection.dynamic_set(None, "other", "value"))

        collection.load_default_dynamic_sets(dynamics_config)

        self.assertEquals(1, len(collection.dynamic_sets))
        self.assertTrue(IsNumeric.NAME in collection.dynamic_sets)

    def test_load_default_dynamic_maps(self):
        dynamics_config = BrainDynamicsConfiguration()

        collection = DynamicsCollection()
        collection.load_default_dynamic_maps(dynamics_config)

        self.assertEquals(4, len(collection.dynamic_maps))
        self.assertTrue(SingularMap.NAME in collection.dynamic_maps)
        self.assertTrue(PluralMap.NAME in collection.dynamic_maps)
        self.assertTrue(SuccessorMap.NAME in collection.dynamic_maps)
        self.assertTrue(PredecessorMap.NAME in collection.dynamic_maps)

        self.assertIsNone(collection.dynamic_map(None, "other", "value"))

        collection.load_default_dynamic_maps(dynamics_config)

        self.assertEquals(4, len(collection.dynamic_maps))
        self.assertTrue(SingularMap.NAME in collection.dynamic_maps)
        self.assertTrue(PluralMap.NAME in collection.dynamic_maps)
        self.assertTrue(SuccessorMap.NAME in collection.dynamic_maps)
        self.assertTrue(PredecessorMap.NAME in collection.dynamic_maps)

    def test_load_default_dynamic_vars(self):
        dynamics_config = BrainDynamicsConfiguration()

        collection = DynamicsCollection()
        collection.load_default_dynamic_vars(dynamics_config)

        self.assertEquals({}, collection.dynamic_sets)

        collection._dynamic_vars["MOCK"] = MockDynamicSettableVariable(None)

        self.assertTrue(collection.set_dynamic_var(None, "MOCK", "MockValue"))
        self.assertFalse(collection.set_dynamic_var(None, "MOCK2", "MockValue"))

        self.assertIsNotNone(collection.dynamic_var(None, "MOCK"))
        self.assertIsNone(collection.dynamic_var(None, "MOCK2"))

    def test_load_default_dynamic_vars_with_exception(self):
        dynamics_config = BrainDynamicsConfiguration()

        collection = DynamicsCollection()
        collection.load_default_dynamic_vars(dynamics_config)

        self.assertEquals({}, collection.dynamic_sets)

        collection._dynamic_vars["MOCK"] = MockDynamicSettableVariable(None, set_exception=True)

        self.assertIsNone(collection.dynamic_var(None, "MOCK"))

    def test_set_dynamic_var_exception(self):
        collection = MockDynamicsCollection()
        collection.set_dynamic_var(None, "MOCK", "MockValue")

import unittest

from programy.dynamic.dynamics import DynamicsCollection
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.brain.dynamic import BrainDynamicsConfiguration
from programy.clients.events.console.config import ConsoleConfiguration

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

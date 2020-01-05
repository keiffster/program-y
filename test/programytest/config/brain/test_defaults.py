import unittest

from programy.clients.events.console.config import ConsoleConfiguration
from programy.config.brain.defaults import BrainDefaultsConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile


class BrainDefaultsDefaultsConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            defaults:
                default_get: unknown
                default_property: unknown
                default_map: unknown
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        defaults_config = BrainDefaultsConfiguration()
        defaults_config.load_config_section(yaml, brain_config, ".")

        self.assertEqual("unknown", defaults_config.default_get)
        self.assertEqual("unknown", defaults_config.default_property)
        self.assertEqual("unknown", defaults_config.default_map)

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            defaults:
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        defaults_config = BrainDefaultsConfiguration()
        defaults_config.load_config_section(yaml, brain_config, ".")

        self.assertEqual("unknown", defaults_config.default_get)
        self.assertEqual("unknown", defaults_config.default_property)
        self.assertEqual("unknown", defaults_config.default_map)

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        defaults_config = BrainDefaultsConfiguration()
        defaults_config.load_config_section(yaml, brain_config, ".")

    def test_defaults(self):
        defaults_config = BrainDefaultsConfiguration()
        data = {}
        defaults_config.to_yaml(data, True)

        BrainDefaultsDefaultsConfigurationTests.assert_defaults(self, data)

    @staticmethod
    def assert_defaults(test, data):
        test.assertEqual(data['default_get'], "unknown")
        test.assertEqual(data['default_property'], "unknown")
        test.assertEqual(data['default_map'], "unknown")

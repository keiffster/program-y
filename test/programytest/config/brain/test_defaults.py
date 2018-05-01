import unittest
import os

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.brain.defaults import BrainDefaultsConfiguration
from programy.clients.events.console.config import ConsoleConfiguration

class BrainDefaultsBinariesConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            defaults:
                default-get: unknown
                default-property: unknown
                default-map: unknown
                learnf-path: /tmp/learnf
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        defaults_config = BrainDefaultsConfiguration()
        defaults_config.load_config_section(yaml, brain_config, ".")

        self.assertEqual("unknown", defaults_config.default_get)
        self.assertEqual("unknown", defaults_config.default_property)
        self.assertEqual("unknown", defaults_config.default_map)
        self.assertEqual("/tmp/learnf", defaults_config.learnf_path)

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
        if os.name == 'posix':
            self.assertEqual('/tmp/learnf', defaults_config.learnf_path)
        elif os.name == 'nt':
            self.assertEqual('C:\Windows\Temp\learnf', defaults_config.learnf_path)

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        defaults_config = BrainDefaultsConfiguration()
        defaults_config.load_config_section(yaml, brain_config, ".")

        if os.name == 'posix':
            self.assertEqual('/tmp/learnf', defaults_config.learnf_path)
        elif os.name == 'nt':
            self.assertEqual('C:\Windows\Temp\learnf', defaults_config.learnf_path)


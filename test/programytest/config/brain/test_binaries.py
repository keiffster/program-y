import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.brain.binaries import BrainBinariesConfiguration
from programy.clients.events.console.config import ConsoleConfiguration

class BrainBinariesConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            binaries:
              save_binary: true
              load_binary: true
              load_aiml_on_binary_fail: true
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        binaries_config = BrainBinariesConfiguration()
        binaries_config.load_config_section(yaml, brain_config, ".")

        self.assertTrue(binaries_config.save_binary)
        self.assertTrue(binaries_config.load_binary)
        self.assertTrue(binaries_config.load_aiml_on_binary_fail)

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            binaries:
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        binaries_config = BrainBinariesConfiguration()
        binaries_config.load_config_section(yaml, brain_config, ".")

        self.assertFalse(binaries_config.save_binary)
        self.assertFalse(binaries_config.load_binary)
        self.assertFalse(binaries_config.load_aiml_on_binary_fail)

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        binaries_config = BrainBinariesConfiguration()
        binaries_config.load_config_section(yaml, brain_config, ".")

        self.assertFalse(binaries_config.save_binary)
        self.assertFalse(binaries_config.load_binary)
        self.assertFalse(binaries_config.load_aiml_on_binary_fail)

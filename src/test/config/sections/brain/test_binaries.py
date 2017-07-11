import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.sections.brain.binaries import BrainBinariesConfiguration
from programy.config.sections.client.console import ConsoleConfiguration

class BrainBinariesConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            binaries:
              save_binary: true
              load_binary: true
              binary_filename: $BOT_ROOT/output/y-bot.brain
              load_aiml_on_binary_fail: true
              dump_to_file: $BOT_ROOT/output/braintree.txt
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        binaries_config = BrainBinariesConfiguration()
        binaries_config.load_config_section(yaml, brain_config, ".")

        self.assertTrue(binaries_config.save_binary)
        self.assertTrue(binaries_config.load_binary)
        self.assertEquals("./output/y-bot.brain", binaries_config.binary_filename)
        self.assertTrue(binaries_config.load_aiml_on_binary_fail)
        self.assertEquals("./output/braintree.txt", binaries_config.dump_to_file)

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
        self.assertIsNone(binaries_config.binary_filename)
        self.assertFalse(binaries_config.load_aiml_on_binary_fail)
        self.assertIsNone(binaries_config.dump_to_file)

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
        self.assertIsNone(binaries_config.binary_filename)
        self.assertFalse(binaries_config.load_aiml_on_binary_fail)
        self.assertIsNone(binaries_config.dump_to_file)

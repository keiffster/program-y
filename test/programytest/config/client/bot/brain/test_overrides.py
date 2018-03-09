import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.brain.overrides import BrainOverridesConfiguration
from programy.clients.events.console.config import ConsoleConfiguration

class BrainDefaultsBinariesConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            overrides:
              allow_system_aiml: true
              allow_learn_aiml: true
              allow_learnf_aiml: true
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        overrides_config = BrainOverridesConfiguration()
        overrides_config.load_config_section(yaml, brain_config, ".")

        self.assertTrue(overrides_config.allow_system_aiml)
        self.assertTrue(overrides_config.allow_learn_aiml)
        self.assertTrue(overrides_config.allow_learnf_aiml)

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            overrides:
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        overrides_config = BrainOverridesConfiguration()
        overrides_config.load_config_section(yaml, brain_config, ".")

        self.assertFalse(overrides_config.allow_system_aiml)
        self.assertFalse(overrides_config.allow_learn_aiml)
        self.assertFalse(overrides_config.allow_learnf_aiml)

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        overrides_config = BrainOverridesConfiguration()
        overrides_config.load_config_section(yaml, brain_config, ".")

        self.assertFalse(overrides_config.allow_system_aiml)
        self.assertFalse(overrides_config.allow_learn_aiml)
        self.assertFalse(overrides_config.allow_learnf_aiml)

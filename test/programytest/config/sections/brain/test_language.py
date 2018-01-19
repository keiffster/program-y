import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.sections.brain.language import BrainLanguageConfiguration
from programy.config.sections.client.console import ConsoleConfiguration

class BrainLanguageConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            language:
              english: true
              chinese: true
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        language_config = BrainLanguageConfiguration()
        language_config.load_config_section(yaml, brain_config, ".")

        self.assertTrue(language_config.english)
        self.assertTrue(language_config.chinese)

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            language:
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        language_config = BrainLanguageConfiguration()
        language_config.load_config_section(yaml, brain_config, ".")

        self.assertTrue(language_config.english)
        self.assertFalse(language_config.chinese)

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        language_config = BrainLanguageConfiguration()
        language_config.load_config_section(yaml, brain_config, ".")

        self.assertTrue(language_config.english)
        self.assertFalse(language_config.chinese)

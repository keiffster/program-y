import unittest

from programy.config.brain.debugfiles import BrainDebugFilesConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.clients.events.console.config import ConsoleConfiguration


class BrainDebugFilesConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            debugfiles:
                save_errors: true
                save_duplicates: true
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        debugfiles_config = BrainDebugFilesConfiguration()

        debugfiles_config.load_config_section(yaml, brain_config, ".")

        self.assertTrue(debugfiles_config.save_errors)
        self.assertTrue(debugfiles_config.save_duplicates)

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            debugfiles:
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        debugfiles_config = BrainDebugFilesConfiguration()

        debugfiles_config.load_config_section(yaml, brain_config, ".")

        self.assertFalse(debugfiles_config.save_errors)
        self.assertFalse(debugfiles_config.save_duplicates)

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        debugfiles_config = BrainDebugFilesConfiguration()

        debugfiles_config.load_config_section(yaml, brain_config, ".")

        self.assertFalse(debugfiles_config.save_errors)
        self.assertFalse(debugfiles_config.save_duplicates)

    def test_defaults(self):
        debugfiles_config = BrainDebugFilesConfiguration()
        data = {}
        debugfiles_config.to_yaml(data, True)

        BrainDebugFilesConfigurationTests.assert_defaults(self, data)

    @staticmethod
    def assert_defaults(test, data):
        test.assertFalse(data['save_errors'])
        test.assertFalse(data['save_duplicates'])

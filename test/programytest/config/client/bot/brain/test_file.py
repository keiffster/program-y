import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.brain.file import BrainFileConfiguration
from programy.clients.events.console.config import ConsoleConfiguration

class BrainFileConfigurationTests(unittest.TestCase):

    def test_with_files_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            files:
                sets:
                    files: $BOT_ROOT/sets
                    extension: .txt
                    directories: false
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")
        self.assertIsNotNone(brain_config)
        files_config = yaml.get_section("files", brain_config)
        self.assertIsNotNone(files_config)

        sets_config = BrainFileConfiguration("sets")
        sets_config.load_config_section(yaml, files_config, ".")

        self.assertEqual(["./sets"], sets_config.files)
        self.assertEqual(".txt", sets_config.extension)
        self.assertFalse(sets_config.directories)

    def test_with_file_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            files:
                sets:
                    file: $BOT_ROOT/sets/test.txt
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")
        self.assertIsNotNone(brain_config)
        files_config = yaml.get_section("files", brain_config)
        self.assertIsNotNone(files_config)

        sets_config = BrainFileConfiguration("sets")
        sets_config.load_config_section(yaml, files_config, ".")

        self.assertEqual("./sets/test.txt", sets_config.file)

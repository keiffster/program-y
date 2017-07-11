import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.sections.brain.aiml_file import BrainAIMLFileConfiguration
from programy.config.sections.client.console import ConsoleConfiguration

class BrainAIMLFileConfigurationTests(unittest.TestCase):

    def test_with_files_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            files:
                aiml:
                    files: $BOT_ROOT/aiml
                    extension: .aiml
                    directories: true
                    errors: $BOT_ROOT/output/y-bot_errors.txt
                    duplicates: $BOT_ROOT/output/y-bot_duplicates.txt
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")
        self.assertIsNotNone(brain_config)
        files_config = yaml.get_section("files", brain_config)
        self.assertIsNotNone(files_config)

        aiml_config = BrainAIMLFileConfiguration()
        aiml_config.load_config_section(yaml, files_config, ".")

        self.assertEqual("./aiml", aiml_config.files)
        self.assertEqual(".aiml", aiml_config.extension)
        self.assertTrue(aiml_config.directories)
        self.assertEqual("./output/y-bot_errors.txt", aiml_config.errors)
        self.assertEqual("./output/y-bot_duplicates.txt", aiml_config.duplicates)

    def test_with_file_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            files:
                aiml:
                    file: $BOT_ROOT/aiml/test.aiml
                    errors: $BOT_ROOT/output/y-bot_errors.txt
                    duplicates: $BOT_ROOT/output/y-bot_duplicates.txt
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")
        self.assertIsNotNone(brain_config)
        files_config = yaml.get_section("files", brain_config)
        self.assertIsNotNone(files_config)

        aiml_config = BrainAIMLFileConfiguration()
        aiml_config.load_config_section(yaml, files_config, ".")

        self.assertEqual("./aiml/test.aiml", aiml_config.file)

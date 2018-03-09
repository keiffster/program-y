import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.brain.aiml_file import BrainAIMLFileConfiguration
from programy.clients.events.console.config import ConsoleConfiguration


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
                    errors:
                      file: /tmp/y-bot-errors.txt
                      format: txt
                      encoding: utf-8
                      delete_on_start: true
                    duplicates:
                      file: /tmp/y-bot-duplicates.txt
                      format: txt
                      encoding: utf-8
                      delete_on_start: true
                    conversation:
                      file: /tmp/y-bot-conversation.csv
                      format: csv
                      delete_on_start: true
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")
        self.assertIsNotNone(brain_config)
        files_config = yaml.get_section("files", brain_config)
        self.assertIsNotNone(files_config)

        aiml_config = BrainAIMLFileConfiguration()
        aiml_config.load_config_section(yaml, files_config, ".")

        self.assertEqual(["./aiml"], aiml_config.files)
        self.assertEqual(".aiml", aiml_config.extension)
        self.assertTrue(aiml_config.directories)
        self.assertEqual("/tmp/y-bot-errors.txt", aiml_config.errors.filename)
        self.assertEqual("/tmp/y-bot-duplicates.txt", aiml_config.duplicates.filename)
        self.assertEqual("/tmp/y-bot-conversation.csv", aiml_config.conversation.filename)

    def test_with_files_multiple_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            files:
                aiml:
                    files: |
                            $BOT_ROOT/aiml
                            $BOT_ROOT/aiml2
                    extension: .aiml
                    directories: true
                    errors: /tmp/y-bot-errors.txt
                    duplicates: /tmp/y-bot-duplicates.txt
                    conversation: /tmp/y-bot-conversation.txt
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")
        self.assertIsNotNone(brain_config)
        files_config = yaml.get_section("files", brain_config)
        self.assertIsNotNone(files_config)

        aiml_config = BrainAIMLFileConfiguration()
        aiml_config.load_config_section(yaml, files_config, ".")

        self.assertEqual(['./aiml', './aiml2'], aiml_config.files)
        self.assertEqual(".aiml", aiml_config.extension)
        self.assertTrue(aiml_config.directories)
        self.assertEqual("/tmp/y-bot-errors.txt", aiml_config.errors.filename)
        self.assertEqual("/tmp/y-bot-duplicates.txt", aiml_config.duplicates.filename)
        self.assertEqual("/tmp/y-bot-conversation.txt", aiml_config.conversation.filename)

    def test_with_file_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            files:
                aiml:
                    file: $BOT_ROOT/aiml/test.aiml
                    errors: /tmp/y-bot-errors.txt
                    duplicates: /tmp/y-bot-duplicates.txt
                    conversation: /tmp/y-bot-conversation.txt
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")
        self.assertIsNotNone(brain_config)
        files_config = yaml.get_section("files", brain_config)
        self.assertIsNotNone(files_config)

        aiml_config = BrainAIMLFileConfiguration()
        aiml_config.load_config_section(yaml, files_config, ".")

        self.assertEqual("./aiml/test.aiml", aiml_config.file)
        self.assertEqual("aiml", aiml_config.extension)
        self.assertFalse(aiml_config.directories)
        self.assertEqual("/tmp/y-bot-errors.txt", aiml_config.errors.filename)
        self.assertEqual("/tmp/y-bot-duplicates.txt", aiml_config.duplicates.filename)
        self.assertEqual("/tmp/y-bot-conversation.txt", aiml_config.conversation.filename)

    def test_with_file_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            files:
                aiml:
                    file: $BOT_ROOT/aiml/test.aiml
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")
        self.assertIsNotNone(brain_config)
        files_config = yaml.get_section("files", brain_config)
        self.assertIsNotNone(files_config)

        aiml_config = BrainAIMLFileConfiguration()
        aiml_config.load_config_section(yaml, files_config, ".")

        self.assertEqual("./aiml/test.aiml", aiml_config.file)
        self.assertEqual("aiml", aiml_config.extension)
        self.assertFalse(aiml_config.directories)
        self.assertIsNone(aiml_config.errors)
        self.assertIsNone(aiml_config.duplicates)
        self.assertIsNone(aiml_config.conversation)

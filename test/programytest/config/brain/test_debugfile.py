import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.brain.debugfile import DebugFileConfiguration
from programy.clients.events.console.config import ConsoleConfiguration

class DebugFileConfigurationTests(unittest.TestCase):

    def test_with_new_format_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            files:
                aiml:
                    errors:
                      file: /tmp/y-bot_errors.csv
                      format: csv
                      encoding: utf-8
                      delete_on_start: true
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")
        self.assertIsNotNone(brain_config)
        files_config = yaml.get_section("files", brain_config)
        self.assertIsNotNone(files_config)
        aiml_config = yaml.get_section("aiml", files_config)
        self.assertIsNotNone(aiml_config)

        debugfile_config = DebugFileConfiguration("errors")
        debugfile_config.load_config_section(yaml, aiml_config, ".")

        self.assertEquals("/tmp/y-bot_errors.csv", debugfile_config.filename)
        self.assertEquals("csv", debugfile_config.file_format)
        self.assertEquals("utf-8", debugfile_config.encoding)
        self.assertTrue(debugfile_config.delete_on_start)

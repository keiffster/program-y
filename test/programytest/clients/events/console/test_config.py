import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.clients.events.console.config import ConsoleConfiguration


class ConsoleConfigurationTests(unittest.TestCase):
    
    def test_init(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
          bot: bot
        """, ConsoleConfiguration(), ".")

        console_config = ConsoleConfiguration()
        console_config.load_configuration(yaml, ".")

        self.assertIsNotNone(console_config.configurations)
        self.assertEquals(1, len(console_config.configurations))

    def test_init_no_values(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
        """, ConsoleConfiguration(), ".")

        console_config = ConsoleConfiguration()
        console_config.load_configuration(yaml, ".")

        self.assertIsNotNone(console_config.configurations)
        self.assertEquals(1, len(console_config.configurations))

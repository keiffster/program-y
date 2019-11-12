import unittest

from programy.clients.events.console.config import ConsoleConfiguration
from programy.clients.events.discord.config import DiscordConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile


class DiscordConfigurationTests(unittest.TestCase):

    def test_init(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        discord:
        """, ConsoleConfiguration(), ".")

        discord_config = DiscordConfiguration()
        discord_config.load_configuration(yaml, ".")

    def test_init_no_values(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        discord:
        """, ConsoleConfiguration(), ".")

        discord_config = DiscordConfiguration()
        discord_config.load_configuration(yaml, ".")

    def test_init_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        other:
        """, ConsoleConfiguration(), ".")

        discord_config = DiscordConfiguration()
        discord_config.load_configuration(yaml, ".")

    def test_to_yaml_with_defaults(self):
        config = DiscordConfiguration()

        data = {}
        config.to_yaml(data, True)


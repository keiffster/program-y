import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.client.config import ClientConfigurationData
from programy.clients.events.console.config import ConsoleConfiguration

class ClientConfigurationDataTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
          bot:  bot
          prompt: ">>>"
          license_keys: $BOT_ROOT/config/license.keys
          bot_selector: programy.clients.client.DefaultBotSelector
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("console")

        client_config = ClientConfigurationData("test")
        client_config.load_configuration(yaml, bot_config, ".")

        self.assertEquals("./config/license.keys", client_config.license_keys)

        self.assertEquals("programy.clients.client.DefaultBotSelector", client_config.bot_selector)

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("console")

        client_config = ClientConfigurationData("test")
        client_config.load_configuration(yaml, bot_config, ".")

        self.assertIsNone(client_config.license_keys)

        self.assertIsNone(client_config.bot_selector)

import unittest

from programy.config.bot.filestorage import BotConversationsFileStorageConfiguration
from programy.clients.events.console.config import ConsoleConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile


class BotConversationsConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
            file_storage:
              dir: $BOT_ROOT/conversations
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("bot")

        convo_config = BotConversationsFileStorageConfiguration(config_name="file_storage")
        convo_config.load_config_section(yaml, bot_config, ".")

        self.assertEquals(convo_config.dir, "./conversations")

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("bot")

        convo_config = BotConversationsFileStorageConfiguration(config_name="file_storage")
        convo_config.load_config_section(yaml, bot_config, ".")

        self.assertIsNone(convo_config.dir)

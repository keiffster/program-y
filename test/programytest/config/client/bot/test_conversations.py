import unittest

from programy.config.bot.conversations import BotConversationsConfiguration
from programy.clients.events.console.config import ConsoleConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile


class BotConversationsConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
            conversations:
              max_histories: 666
              initial_topic: topic1
              restore_last_topic: true
              type: file
              config_name: file_storage
        
            file_storage:
              dir: $BOT_ROOT/conversations
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("bot")

        convo_config = BotConversationsConfiguration()
        convo_config.load_config_section(yaml, bot_config, ".")

        self.assertEquals(convo_config.section_name, "conversations")

        self.assertEquals(666, convo_config.max_histories)
        self.assertEquals("topic1", convo_config.initial_topic)
        self.assertTrue(convo_config.restore_last_topic)

        self.assertEquals(convo_config.type, "file")
        self.assertIsNotNone(convo_config.storage)

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("bot")

        convo_config = BotConversationsConfiguration()
        convo_config.load_config_section(yaml, bot_config, ".")

        self.assertEquals(convo_config.section_name, "conversations")

        self.assertEquals(100, convo_config.max_histories)
        self.assertEquals("*", convo_config.initial_topic)
        self.assertFalse(convo_config.restore_last_topic)

        self.assertIsNone(convo_config.type)
        self.assertIsNone(convo_config.storage)

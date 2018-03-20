import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.bot.redisstorage import BotConversationsRedisStorageConfiguration
from programy.clients.events.console.config import ConsoleConfiguration

class RedisStorageConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
            redis:
                host: localhost
                port: 6379
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("bot")

        redis_config = BotConversationsRedisStorageConfiguration("redis")
        redis_config.load_config_section(yaml, bot_config, ".")

        self.assertEquals("localhost", redis_config.host)
        self.assertEquals(6379, redis_config.port)

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
            redis:
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("bot")

        redis_config = BotConversationsRedisStorageConfiguration("redis")
        redis_config.load_config_section(yaml, bot_config, ".")

        self.assertEquals("localhost", redis_config.host)
        self.assertEquals(6379, redis_config.port)

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("bot")

        redis_config = BotConversationsRedisStorageConfiguration("redis")
        redis_config.load_config_section(yaml, bot_config, ".")

        self.assertEquals("localhost", redis_config.host)
        self.assertEquals(6379, redis_config.port)

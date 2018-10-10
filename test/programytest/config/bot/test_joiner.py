import unittest
import os

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.bot.joiner import BotSentenceJoinerConfiguration
from programy.clients.events.console.config import ConsoleConfiguration

class BotSentenceJoinerConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
            joiner:
                classname: programy.dialog.joiner.SentenceJoiner
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("bot")

        joiner_config = BotSentenceJoinerConfiguration()
        joiner_config.load_config_section(yaml, bot_config, ".")

        self.assertEqual("programy.dialog.joiner.SentenceJoiner", joiner_config.classname)
        self.assertEqual('.?!', joiner_config.join_chars)
        self.assertEqual('.', joiner_config.terminator)

    def test_with_default_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
            joiner:
                classname: programy.dialog.joiner.SentenceJoiner
                join_chars: .?!
                termiantor: .
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("bot")

        joiner_config = BotSentenceJoinerConfiguration()
        joiner_config.load_config_section(yaml, bot_config, ".")

        self.assertEqual("programy.dialog.joiner.SentenceJoiner", joiner_config.classname)
        self.assertEqual(".?!", joiner_config.join_chars)
        self.assertEqual('.', joiner_config.terminator)

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
            joiner:
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("bot")

        joiner_config = BotSentenceJoinerConfiguration()
        joiner_config.load_config_section(yaml, bot_config, ".")

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("bot")

        joiner_config = BotSentenceJoinerConfiguration()
        joiner_config.load_config_section(yaml, bot_config, ".")


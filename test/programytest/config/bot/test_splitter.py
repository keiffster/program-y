import unittest

from programy.clients.events.console.config import ConsoleConfiguration
from programy.config.bot.splitter import BotSentenceSplitterConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.utils.license.keys import LicenseKeys


class BotSentenceSplitterConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
            splitter:
                classname: programy.dialog.splitter.regex.RegexSentenceSplitter
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("bot")

        splitter_config = BotSentenceSplitterConfiguration()
        splitter_config.load_config_section(yaml, bot_config, ".")

        license_keys = LicenseKeys()
        splitter_config.check_for_license_keys(license_keys)

        self.assertEqual("programy.dialog.splitter.regex.RegexSentenceSplitter", splitter_config.classname)
        self.assertEqual('[:;,.?!]', splitter_config.split_chars)

    def test_with_default_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
            splitter:
                classname: programy.dialog.splitter.regex.RegexSentenceSplitter
                split_chars: .:'
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("bot")

        splitter_config = BotSentenceSplitterConfiguration()
        splitter_config.load_config_section(yaml, bot_config, ".")

        self.assertEqual("programy.dialog.splitter.regex.RegexSentenceSplitter", splitter_config.classname)
        self.assertEqual(".:'", splitter_config.split_chars)

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
            splitter:
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("bot")

        splitter_config = BotSentenceSplitterConfiguration()
        splitter_config.load_config_section(yaml, bot_config, ".")

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("bot")

        splitter_config = BotSentenceSplitterConfiguration()
        splitter_config.load_config_section(yaml, bot_config, ".")

    def test_defaults(self):
        splitter_config = BotSentenceSplitterConfiguration()
        data = {}
        splitter_config.to_yaml(data, True)

        BotSentenceSplitterConfigurationTests.assert_defaults(self, data)

    @staticmethod
    def assert_defaults(test, data):
        test.assertEqual(data['classname'], BotSentenceSplitterConfiguration.DEFAULT_CLASSNAME)
        test.assertEqual(data['split_chars'], BotSentenceSplitterConfiguration.DEFAULT_SPLITCHARS)

import unittest

from programy.clients.events.console.config import ConsoleConfiguration
from programy.config.bot.spelling import BotSpellingConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.utils.license.keys import LicenseKeys


class BotSpellingConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
            spelling:
              classname: programy.spelling.norvig.NorvigSpellingChecker
              alphabet: abcdefghijklmnopqrstuvwxyz
              check_before: true
              check_and_retry: true
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("bot")

        spelling_config = BotSpellingConfiguration()
        spelling_config.load_config_section(yaml, bot_config, ".")

        license_keys = LicenseKeys()
        spelling_config.check_for_license_keys(license_keys)

        self.assertEqual("programy.spelling.norvig.NorvigSpellingChecker", spelling_config.classname)
        self.assertEqual("abcdefghijklmnopqrstuvwxyz", spelling_config.alphabet)
        self.assertTrue(spelling_config.check_before)
        self.assertTrue(spelling_config.check_and_retry)

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
            spelling:
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("bot")

        spelling_config = BotSpellingConfiguration()
        spelling_config.load_config_section(yaml, bot_config, ".")

        self.assertIsNone(spelling_config.classname)
        self.assertIsNone(spelling_config.alphabet)
        self.assertFalse(spelling_config.check_before)
        self.assertFalse(spelling_config.check_and_retry)

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("bot")

        spelling_config = BotSpellingConfiguration()
        spelling_config.load_config_section(yaml, bot_config, ".")

        self.assertIsNone(spelling_config.classname)
        self.assertIsNone(spelling_config.alphabet)
        self.assertFalse(spelling_config.check_before)
        self.assertFalse(spelling_config.check_and_retry)

    def test_defaults(self):
        spelling_config = BotSpellingConfiguration()
        data = {}
        spelling_config.to_yaml(data, True)

        BotSpellingConfigurationTests.assert_defaults(self, data)

    @staticmethod
    def assert_defaults(test, data):
        test.assertEqual(data['classname'], "programy.spelling.norvig.NorvigSpellingChecker")
        test.assertEqual(data['alphabet'], 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        test.assertEqual(data['check_before'], False)
        test.assertEqual(data['check_and_retry'], False)

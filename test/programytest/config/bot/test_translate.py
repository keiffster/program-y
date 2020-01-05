import unittest

from programy.clients.events.console.config import ConsoleConfiguration
from programy.config.bot.translation import BotTranslatorConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.utils.license.keys import LicenseKeys


class BotTranslatorConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
            translator:
                classname: programy.nlp.translate.textblob_translator.TextBlobTranslator
                from: fr
                to: en 
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("bot")

        translator_config = BotTranslatorConfiguration(name="translator")
        translator_config.load_config_section(yaml, bot_config, ".")

        license_keys = LicenseKeys()
        translator_config.check_for_license_keys(license_keys)

        self.assertEqual("programy.nlp.translate.textblob_translator.TextBlobTranslator", translator_config.classname)
        self.assertEqual("en", translator_config.to_lang)
        self.assertEqual("fr", translator_config.from_lang)

    def test_with_default_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
            translator:
                classname: programy.nlp.translate.textblob_translator.TextBlobTranslator
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("bot")

        translator_config = BotTranslatorConfiguration(name="translator")
        translator_config.load_config_section(yaml, bot_config, ".")

        self.assertEqual("programy.nlp.translate.textblob_translator.TextBlobTranslator", translator_config.classname)
        self.assertIsNone(translator_config.to_lang)
        self.assertIsNone(translator_config.from_lang)

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
            translator:
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("bot")

        translator_config = BotTranslatorConfiguration(name="translator")
        translator_config.load_config_section(yaml, bot_config, ".")

        self.assertIsNone(translator_config.classname)
        self.assertIsNone(translator_config.from_lang)
        self.assertIsNone(translator_config.to_lang)

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("bot")

        translator_config = BotTranslatorConfiguration(name="translator")
        translator_config.load_config_section(yaml, bot_config, ".")

        self.assertIsNone(translator_config.classname)
        self.assertIsNone(translator_config.from_lang)
        self.assertIsNone(translator_config.to_lang)

    def test_defaults(self):
        translator_config = BotTranslatorConfiguration(name="translator")
        data = {}
        translator_config.to_yaml(data, True)

        BotTranslatorConfigurationTests.assert_defaults(self, data)

    @staticmethod
    def assert_defaults(test, data):
        test.assertEqual(data['classname'], "programy.nlp.translate.textblob_translator.TextBlobTranslator")
        test.assertEqual(data['from'], None)
        test.assertEqual(data['to'], None)

import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.clients.polling.telegram.config import TelegramConfiguration
from programy.clients.events.console.config import ConsoleConfiguration

class TelegramClientConfigurationTests(unittest.TestCase):

    def test_init(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
            telegram:
              unknown_command: Sorry, that is not a command I have been taught yet!
              unknown_command_srai: YTELEGRAM_UNKNOWN_COMMAND
          """, ConsoleConfiguration(), ".")

        telegram_config = TelegramConfiguration()
        telegram_config.load_configuration(yaml, ".")

        self.assertEqual(telegram_config.unknown_command, "Sorry, that is not a command I have been taught yet!")
        self.assertEqual(telegram_config.unknown_command_srai, "YTELEGRAM_UNKNOWN_COMMAND")

    def test_to_yaml_with_defaults(self):
        config = TelegramConfiguration()

        data = {}
        config.to_yaml(data, True)

        self.assertEqual('Sorry, that is not a command I have been taught yet!', data['unknown_command'])
        self.assertEqual('YTELEGRAM_UNKNOWN_COMMAND', data['unknown_command_srai'])

        self.assertEqual(data['bot'], 'bot')
        self.assertEqual(data['bot_selector'], "programy.clients.client.DefaultBotSelector")
        self.assertEqual(data['renderer'], "programy.clients.render.text.TextRenderer")

import unittest

from programy.clients.events.console.config import ConsoleConfiguration
from programy.clients.restful.asyncio.microsoft.config import MicrosoftConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile


class MicrosoftConfigurationTests(unittest.TestCase):

    def test_init(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        microsoft:
          host: 127.0.0.1
          port: 5000
          debug: false
          new_user_text: Hello new user
          new_user_srai: NEW_USER_SRAI
        """, ConsoleConfiguration(), ".")

        microsoft_config = MicrosoftConfiguration()
        microsoft_config.load_configuration(yaml, ".")

        self.assertEqual("127.0.0.1", microsoft_config.host)
        self.assertEqual(5000, microsoft_config.port)
        self.assertEqual(False, microsoft_config.debug)
        self.assertEqual("Hello new user", microsoft_config.new_user_text)
        self.assertEqual("NEW_USER_SRAI", microsoft_config.new_user_srai)

    def test_init_no_values(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        microsoft:
        """, ConsoleConfiguration(), ".")

        microsoft_config = MicrosoftConfiguration()
        microsoft_config.load_configuration(yaml, ".")

        self.assertEqual("0.0.0.0", microsoft_config.host)
        self.assertEqual(80, microsoft_config.port)
        self.assertEqual(False, microsoft_config.debug)
        self.assertEqual( MicrosoftConfiguration.NEW_USER_TEXT, microsoft_config.new_user_text)
        self.assertIsNone(microsoft_config.new_user_srai)

    def test_to_yaml_with_defaults(self):
        config = MicrosoftConfiguration()

        data = {}
        config.to_yaml(data, True)

        self.assertEqual(data['bot_selector'], "programy.clients.botfactory.DefaultBotSelector")
        self.assertEqual(data['renderer'], "programy.clients.render.text.TextRenderer")

        self.assertTrue('bots' in data)
        self.assertTrue('bot' in data['bots'])
        self.assertEqual(data['bot_selector'], "programy.clients.botfactory.DefaultBotSelector")

        self.assertTrue('brains' in data['bots']['bot'])
        self.assertTrue('brain' in data['bots']['bot']['brains'])

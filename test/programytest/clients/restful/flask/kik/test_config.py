import unittest

from programy.clients.events.console.config import ConsoleConfiguration
from programy.clients.restful.flask.kik.config import KikConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile


class KikConfigurationTests(unittest.TestCase):

    def test_init(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        kik:
          bot_name: testbot
          webhook: https://localhost:5000
          host: 127.0.0.1
          port: 5000
          debug: false
          unknown_command: Sorry, that is not a command I have been taught yet!
          unknown_command_srai: YKIK_UNKNOWN_COMMAND
        """, ConsoleConfiguration(), ".")

        kik_config = KikConfiguration()
        kik_config.load_configuration(yaml, ".")

        self.assertEqual("testbot", kik_config.bot_name)
        self.assertEqual("https://localhost:5000", kik_config.webhook)
        self.assertEqual("127.0.0.1", kik_config.host)
        self.assertEqual(5000, kik_config.port)
        self.assertEqual(False, kik_config.debug)
        self.assertEqual(kik_config.unknown_command, "Sorry, that is not a command I have been taught yet!")
        self.assertEqual(kik_config.unknown_command_srai, "YKIK_UNKNOWN_COMMAND")

    def test_init_no_values(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        kik:
        """, ConsoleConfiguration(), ".")

        kik_config = KikConfiguration()
        kik_config.load_configuration(yaml, ".")

        self.assertEqual("program-y", kik_config.bot_name)
        self.assertEqual("https://localhost:5000", kik_config.webhook)
        self.assertEqual("0.0.0.0", kik_config.host)
        self.assertEqual(80, kik_config.port)
        self.assertEqual(False, kik_config.debug)

    def test_init_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        client:
        """, ConsoleConfiguration(), ".")

        kik_config = KikConfiguration()
        kik_config.load_configuration(yaml, ".")

        self.assertEqual("program-y", kik_config.bot_name)
        self.assertEqual("https://localhost:5000", kik_config.webhook)
        self.assertEqual("0.0.0.0", kik_config.host)
        self.assertEqual(80, kik_config.port)
        self.assertEqual(False, kik_config.debug)

    def test_to_yaml_with_defaults(self):
        config = KikConfiguration()

        data = {}
        config.to_yaml(data, True)

        self.assertEqual(data['bot_name'], "program-y")
        self.assertEqual(data['webhook'], "https://666666666.ngrok.io")
        self.assertEqual(data['unknown_command'], "Unknown command")
        self.assertEqual(data['unknown_command_srai'], 'KIKUNKNONWCOMMAND')

        self.assertEqual(data['bot_selector'], "programy.clients.botfactory.DefaultBotSelector")
        self.assertEqual(data['renderer'], "programy.clients.render.text.TextRenderer")

        self.assertTrue('bots' in data)
        self.assertTrue('bot' in data['bots'])
        self.assertEqual(data['bot_selector'], "programy.clients.botfactory.DefaultBotSelector")

        self.assertTrue('brains' in data['bots']['bot'])
        self.assertTrue('brain' in data['bots']['bot']['brains'])

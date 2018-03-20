import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.clients.restful.flask.kik.config  import KikConfiguration
from programy.clients.events.console.config import ConsoleConfiguration

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
        self.assertEquals(kik_config.unknown_command, "Sorry, that is not a command I have been taught yet!")
        self.assertEquals(kik_config.unknown_command_srai, "YKIK_UNKNOWN_COMMAND")

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

import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.sections.client.kik_client import KikConfiguration
from programy.config.sections.client.console import ConsoleConfiguration

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
        """, ConsoleConfiguration(), ".")

        kik_config = KikConfiguration()
        kik_config.load_configuration(yaml, ".")

        self.assertEqual("testbot", kik_config.bot_name)
        self.assertEqual("https://localhost:5000", kik_config.webhook)
        self.assertEqual("127.0.0.1", kik_config.host)
        self.assertEqual(5000, kik_config.port)
        self.assertEqual(False, kik_config.debug)

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
        self.assertEqual(5000, kik_config.port)
        self.assertEqual(False, kik_config.debug)

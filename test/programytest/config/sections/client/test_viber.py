import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.sections.client.viber_client import ViberConfiguration
from programy.config.sections.client.console import ConsoleConfiguration

class ViberConfigurationTests(unittest.TestCase):

    def test_init(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        viber:
          host: 127.0.0.1
          port: 5000
          debug: false
          name: test
          avatar: avatar.jpg
          webhook: http://localhost
        """, ConsoleConfiguration(), ".")

        viber_config = ViberConfiguration()
        viber_config.load_configuration(yaml, ".")

        self.assertEqual("127.0.0.1", viber_config.host)
        self.assertEqual(5000, viber_config.port)
        self.assertEqual(False, viber_config.debug)
        self.assertEqual("test", viber_config.name)
        self.assertEqual("avatar.jpg", viber_config.avatar)
        self.assertEqual("http://localhost", viber_config.webhook)

    def test_init_no_values(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        viber:
        """, ConsoleConfiguration(), ".")

        viber_config = ViberConfiguration()
        viber_config.load_configuration(yaml, ".")

        self.assertEqual("0.0.0.0", viber_config.host)
        self.assertEqual(5001, viber_config.port)
        self.assertEqual(False, viber_config.debug)
        self.assertIsNone(viber_config.name)
        self.assertIsNone(viber_config.avatar)
        self.assertIsNone(viber_config.webhook)

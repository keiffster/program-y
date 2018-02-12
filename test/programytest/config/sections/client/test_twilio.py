import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.sections.client.twilio import TwilioConfiguration
from programy.config.sections.client.console import ConsoleConfiguration

class TwilioConfigurationTests(unittest.TestCase):

    def test_init(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        twilio:
          host: 127.0.0.1
          port: 5000
          debug: false
        """, ConsoleConfiguration(), ".")

        twilio_config = TwilioConfiguration()
        twilio_config.load_configuration(yaml, ".")

        self.assertEqual("127.0.0.1", twilio_config.host)
        self.assertEqual(5000, twilio_config.port)
        self.assertEqual(False, twilio_config.debug)

    def test_init_no_values(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        twilio:
        """, ConsoleConfiguration(), ".")

        twilio_config = TwilioConfiguration()
        twilio_config.load_configuration(yaml, ".")

        self.assertEqual("0.0.0.0", twilio_config.host)
        self.assertEqual(5001, twilio_config.port)
        self.assertEqual(False, twilio_config.debug)

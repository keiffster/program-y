import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.clients.restful.flask.twilio.config import TwilioConfiguration
from programy.clients.events.console.config import ConsoleConfiguration

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
        self.assertEqual(80, twilio_config.port)
        self.assertEqual(False, twilio_config.debug)

    def test_to_yaml_with_defaults(self):
        config = TwilioConfiguration()

        data = {}
        config.to_yaml(data, True)

        self.assertEqual(data['bot'], 'bot')
        self.assertEqual(data['bot_selector'], "programy.clients.client.DefaultBotSelector")
        self.assertEqual(data['renderer'], "programy.clients.render.text.TextRenderer")

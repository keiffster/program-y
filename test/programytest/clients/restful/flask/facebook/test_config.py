import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.clients.restful.flask.facebook.config import FacebookConfiguration
from programy.clients.events.console.config import ConsoleConfiguration


class FacebookConfigurationTests(unittest.TestCase):

    def test_init(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        facebook:
          host: 127.0.0.1
          port: 5000
          debug: false
        """, ConsoleConfiguration(), ".")

        facebook_config = FacebookConfiguration()
        facebook_config.load_configuration(yaml, ".")

        self.assertEqual("127.0.0.1", facebook_config.host)
        self.assertEqual(5000, facebook_config.port)
        self.assertEqual(False, facebook_config.debug)

    def test_init_no_values(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        facebook:
        """, ConsoleConfiguration(), ".")

        facebook_config = FacebookConfiguration()
        facebook_config.load_configuration(yaml, ".")

        self.assertEqual("0.0.0.0", facebook_config.host)
        self.assertEqual(80, facebook_config.port)
        self.assertEqual(False, facebook_config.debug)

    def test_to_yaml_with_defaults(self):
        config = FacebookConfiguration()

        data = {}
        config.to_yaml(data, True)

        self.assertEquals(data['bot'], 'bot')
        self.assertEquals(data['license_keys'], "./config/license.keys")
        self.assertEquals(data['bot_selector'], "programy.clients.client.DefaultBotSelector")
        self.assertEquals(data['renderer'], "programy.clients.render.text.TextRenderer")

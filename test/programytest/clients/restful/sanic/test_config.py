import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.clients.restful.sanic.config import SanicRestConfiguration
from programy.clients.events.console.config import ConsoleConfiguration

class SanicRestConfigurationTests(unittest.TestCase):

    def test_init(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        sanic:
          host: 127.0.0.1
          port: 5000
          debug: false
          workers: 4
          use_api_keys: false
          api_key_file: apikeys.txt
        """, ConsoleConfiguration(), ".")

        sanic_config = SanicRestConfiguration("sanic")
        sanic_config.load_configuration(yaml, ".")

        self.assertEqual("127.0.0.1", sanic_config.host)
        self.assertEqual(5000, sanic_config.port)
        self.assertEqual(False, sanic_config.debug)
        self.assertEqual(False, sanic_config.use_api_keys)
        self.assertEqual("apikeys.txt", sanic_config.api_key_file)

        self.assertEqual(4, sanic_config.workers)

    def test_init_no_values(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        rest:
        """, ConsoleConfiguration(), ".")

        sanic_config = SanicRestConfiguration("rest")
        sanic_config.load_configuration(yaml, ".")

        self.assertEqual("0.0.0.0", sanic_config.host)
        self.assertEqual(80, sanic_config.port)
        self.assertEqual(False, sanic_config.debug)
        self.assertEqual(False, sanic_config.use_api_keys)

    def test_to_yaml_with_defaults(self):
        config = SanicRestConfiguration("sanic")

        data = {}
        config.to_yaml(data, True)

        self.assertEqual(data['workers'], 4)

        self.assertEqual(data['bot'], 'bot')
        self.assertEqual(data['bot_selector'], "programy.clients.client.DefaultBotSelector")
        self.assertEqual(data['renderer'], "programy.clients.render.text.TextRenderer")

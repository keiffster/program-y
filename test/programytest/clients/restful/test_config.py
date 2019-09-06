import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.clients.restful.config import RestConfiguration
from programy.clients.events.console.config import ConsoleConfiguration


class RestConfigurationTests(unittest.TestCase):

    def test_init_without_auth(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        rest:
          host: 127.0.0.1
          port: 5000
          debug: false
          workers: 4
          use_api_keys: false
          api_key_file: apikeys.txt
        """, ConsoleConfiguration(), ".")

        rest_config = RestConfiguration("rest")
        rest_config.load_configuration(yaml, ".")

        self.assertEqual("127.0.0.1", rest_config.host)
        self.assertEqual(5000, rest_config.port)
        self.assertEqual(False, rest_config.debug)
        self.assertEqual(False, rest_config.use_api_keys)
        self.assertEqual("apikeys.txt", rest_config.api_key_file)
        self.assertIsNone(rest_config.authorization)

    def test_init_with_auth(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        rest:
          host: 127.0.0.1
          port: 5000
          debug: false
          workers: 4
          use_api_keys: false
          api_key_file: apikeys.txt
          authorization: Basic
        """, ConsoleConfiguration(), ".")

        rest_config = RestConfiguration("rest")
        rest_config.load_configuration(yaml, ".")

        self.assertEqual("127.0.0.1", rest_config.host)
        self.assertEqual(5000, rest_config.port)
        self.assertEqual(False, rest_config.debug)
        self.assertEqual(False, rest_config.use_api_keys)
        self.assertEqual("apikeys.txt", rest_config.api_key_file)
        self.assertEqual("Basic", rest_config.authorization)

    def test_init_no_values(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        rest:
        """, ConsoleConfiguration(), ".")

        rest_config = RestConfiguration("rest")
        rest_config.load_configuration(yaml, ".")

        self.assertEqual("0.0.0.0", rest_config.host)
        self.assertEqual(80, rest_config.port)
        self.assertEqual(False, rest_config.debug)
        self.assertEqual(False, rest_config.use_api_keys)
        self.assertIsNone(rest_config.authorization)

    def test_to_yaml_with_defaults(self):
        config = RestConfiguration("rest")

        data = {}
        config.to_yaml(data, True)

        self.assertEqual(data['host'], "0.0.0.0")
        self.assertEqual(data['port'], 80)
        self.assertEqual(data['debug'], False)
        self.assertIsNone(data['authorization'])
        self.assertEqual(data['use_api_keys'], False)
        self.assertEqual(data['ssl_key_file'], './rsa.keys')
        self.assertEqual(data['api_key_file'], './api.keys')
        self.assertEqual(data['ssl_cert_file'], './rsa.cert')
        self.assertEqual(data['ssl_key_file'], './rsa.keys')

        self.assertEqual(data['bot'], 'bot')
        self.assertEqual(data['bot_selector'], "programy.clients.client.DefaultBotSelector")
        self.assertEqual(data['renderer'], "programy.clients.render.text.TextRenderer")

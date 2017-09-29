import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.sections.client.rest import RestConfiguration
from programy.config.sections.client.console import ConsoleConfiguration

class RestConfigurationTests(unittest.TestCase):

    def test_init(self):
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

        rest_config = RestConfiguration()
        rest_config.load_configuration(yaml, ".")

        self.assertEqual("127.0.0.1", rest_config.host)
        self.assertEqual(5000, rest_config.port)
        self.assertEqual(False, rest_config.debug)
        self.assertEqual(4, rest_config.workers)
        self.assertEqual(False, rest_config.use_api_keys)
        self.assertEqual("apikeys.txt", rest_config.api_key_file)

    def test_init_no_values(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        rest:
        """, ConsoleConfiguration(), ".")

        rest_config = RestConfiguration()
        rest_config.load_configuration(yaml, ".")

        self.assertEqual("0.0.0.0", rest_config.host)
        self.assertEqual(80, rest_config.port)
        self.assertEqual(False, rest_config.debug)
        self.assertEqual(4, rest_config.workers)
        self.assertEqual(False, rest_config.use_api_keys)

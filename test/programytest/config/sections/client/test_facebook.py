import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.sections.client.facebook import FacebookConfiguration
from programy.config.sections.client.console import ConsoleConfiguration

class FacebookConfigurationTests(unittest.TestCase):

    def test_init(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
            facebook:
              polling: true
              polling_interval: 30
              streaming: true
        """, ConsoleConfiguration(), ".")

        facebook_config = FacebookConfiguration()
        facebook_config.load_config_section(yaml, ".")

        self.assertTrue(facebook_config.polling)
        self.assertEqual(30, facebook_config.polling_interval)
        self.assertTrue(facebook_config.streaming)


import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.sections.client.slack_client import SlackConfiguration
from programy.config.sections.client.console import ConsoleConfiguration


class SlackConfigurationTests(unittest.TestCase):

    def test_init(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
            slack:
              polling_interval: 1
        """, ConsoleConfiguration(), ".")

        slack_config = SlackConfiguration()
        slack_config.load_configuration(yaml, ".")

        self.assertEqual(1, slack_config.polling_interval)


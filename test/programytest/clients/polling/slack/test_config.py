import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.clients.polling.slack.config import SlackConfiguration
from programy.clients.events.console.config import ConsoleConfiguration


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

    def test_to_yaml_with_defaults(self):
        config = SlackConfiguration()

        data = {}
        config.to_yaml(data, True)

        self.assertEquals(1, data['polling_interval'])

        self.assertEquals(data['bot'], 'bot')
        self.assertEquals(data['license_keys'], "./config/license.keys")
        self.assertEquals(data['bot_selector'], "programy.clients.client.DefaultBotSelector")
        self.assertEquals(data['renderer'], "programy.clients.render.text.TextRenderer")

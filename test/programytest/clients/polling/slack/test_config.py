import unittest

from programy.clients.events.console.config import ConsoleConfiguration
from programy.clients.polling.slack.config import SlackConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile


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

        self.assertEqual(1, data['polling_interval'])

        self.assertEqual(data['bot_selector'], "programy.clients.botfactory.DefaultBotSelector")
        self.assertEqual(data['renderer'], "programy.clients.render.text.TextRenderer")

        self.assertTrue('bots' in data)
        self.assertTrue('bot' in data['bots'])
        self.assertEqual(data['bot_selector'], "programy.clients.botfactory.DefaultBotSelector")

        self.assertTrue('brains' in data['bots']['bot'])
        self.assertTrue('brain' in data['bots']['bot']['brains'])

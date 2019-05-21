import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.brain.openchatbot import BrainOpenChatBotConfiguration
from programy.clients.events.console.config import ConsoleConfiguration


class BrainOpenChatBotConfigurationTests(unittest.TestCase):

    def test_rest_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            openchatbots:
                chatbot1:
                    url: https://99.88.77.66/api/rest/v2.0/ask
                    method: GET
                    authorization: Basic
                    api_key: '11111111'
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")
        self.assertIsNotNone(brain_config)
        openchatbots_config = yaml.get_section("openchatbots", brain_config)
        self.assertIsNotNone(openchatbots_config)

        openchatbot_config = BrainOpenChatBotConfiguration("chatbot1")
        openchatbot_config.load_config_section(yaml, openchatbots_config, ".")

        self.assertEqual("GET", openchatbot_config.method)
        self.assertEqual("https://99.88.77.66/api/rest/v2.0/ask", openchatbot_config.url)
        self.assertEqual("Basic", openchatbot_config.authorization)
        self.assertEqual("11111111", openchatbot_config.api_key)

    def test_rest_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            openchatbots:
                chatbot1:
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")
        self.assertIsNotNone(brain_config)
        openchatbots_config = yaml.get_section("openchatbots", brain_config)
        self.assertIsNotNone(openchatbots_config)

        openchatbot_config = BrainOpenChatBotConfiguration("chatbot1")
        openchatbot_config.load_config_section(yaml, openchatbots_config, ".")

        self.assertIsNone(openchatbot_config.url)
        self.assertIsNone(openchatbot_config.method)
        self.assertIsNone(openchatbot_config.authorization)
        self.assertIsNone(openchatbot_config.api_key)



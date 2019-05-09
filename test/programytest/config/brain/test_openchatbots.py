import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.brain.openchatbots import BrainOpenChatBotsConfiguration
from programy.clients.events.console.config import ConsoleConfiguration


class BrainOpenChatBotsConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            openchatbots:
                chatbot1:
                    url: https://11.11.11.11/api/rest/v2.0/ask
                    method: GET
                chatbot2:
                    url: https://22.22.22.22/api/rest/v2.0/ask
                    method: GET
                chatbot3:
                    url: https://33.33.33.33/api/rest/v2.0/ask
                    method: POST
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        openchatbots_config = BrainOpenChatBotsConfiguration()
        openchatbots_config.load_config_section(yaml, brain_config, ".")

        self.assertTrue(openchatbots_config.exists("chatbot1"))
        self.assertTrue(openchatbots_config.exists("chatbot2"))
        self.assertTrue(openchatbots_config.exists("chatbot3"))
        self.assertFalse(openchatbots_config.exists("chatbot4"))

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            openchatbots:
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        openchatbots_config = BrainOpenChatBotsConfiguration()
        openchatbots_config.load_config_section(yaml, brain_config, ".")

        self.assertFalse(openchatbots_config.exists("REST"))
        self.assertFalse(openchatbots_config.exists("Pannous"))
        self.assertFalse(openchatbots_config.exists("Pandora"))
        self.assertFalse(openchatbots_config.exists("Wikipedia"))
        self.assertFalse(openchatbots_config.exists("Other"))

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        openchatbots_config = BrainOpenChatBotsConfiguration()
        openchatbots_config.load_config_section(yaml, brain_config, ".")

        self.assertFalse(openchatbots_config.exists("REST"))
        self.assertFalse(openchatbots_config.exists("Pannous"))
        self.assertFalse(openchatbots_config.exists("Pandora"))
        self.assertFalse(openchatbots_config.exists("Wikipedia"))
        self.assertFalse(openchatbots_config.exists("Other"))

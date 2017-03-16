import unittest

from programy.config.bot import BotConfiguration
from programy.config.file.yaml import YamlConfigurationFile
from programy.config.client.client import ClientConfiguration


class BotConfigurationTests(unittest.TestCase):

    def test_init(self):
        client_config = ClientConfiguration()
        yaml = YamlConfigurationFile(client_config)
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
            prompt: ">>>"
            initial_question: Hi, how can I help you today?
            default_response: Sorry, I don't have an answer for that!
            exit_response: So long, and thanks for the fish!
        """, ".")

        bot_config = BotConfiguration()
        bot_config.load_config_section(yaml, ".")

        self.assertEqual(">>>", bot_config.prompt)
        self.assertEqual("Hi, how can I help you today?", bot_config.initial_question)
        self.assertEqual("Sorry, I don't have an answer for that!", bot_config.default_response)
        self.assertEqual("So long, and thanks for the fish!", bot_config.exit_response)



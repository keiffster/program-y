import unittest

from programy.config.bot import BotConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.client.client import ClientConfiguration


class BotConfigurationTests(unittest.TestCase):

    def test_init(self):
        client_config = ClientConfiguration()
        yaml = YamlConfigurationFile(client_config)
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
            license_keys: $BOT_ROOT/config/license.keys
            prompt: ">>>"
            initial_question: Hi, how can I help you today?
            default_response: Sorry, I don't have an answer for that!
            empty_string: YEMPTY
            exit_response: So long, and thanks for the fish!
            override_predicates: true
            max_recursion: 10

        """, ".")

        bot_config = BotConfiguration()
        bot_config.load_config_section(yaml, ".")

        self.assertEqual("./config/license.keys", bot_config.license_keys)
        self.assertEqual(">>>", bot_config.prompt)
        self.assertEqual("Hi, how can I help you today?", bot_config.initial_question)
        self.assertEqual("Sorry, I don't have an answer for that!", bot_config.default_response)
        self.assertEqual("YEMPTY", bot_config.empty_string)

        self.assertEqual(10, bot_config.max_recursion)

        self.assertTrue(bot_config.override_predicates)



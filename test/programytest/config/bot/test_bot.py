import unittest

from programy.config.bot.bot import BotConfiguration
from programy.clients.events.console.config import ConsoleConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile


class BotConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
            brain_selector: programy.bot.DefaultBrainSelector
        
            prompt: ">>>"
            initial_question: Hi, how can I help you today?
            initial_question_srai: YINITIALQUESTION
            default_response: Sorry, I don't have an answer for that!
            default_response_srai: YDEFAULTRESPONSE
            empty_string: YEMPTY
            exit_response: So long, and thanks for the fish!
            exit_response_srai: YEXITRESPONSE
            override_properties: true
            max_question_recursion: 1000
            max_question_timeout: 60
            max_search_depth: 100
            max_search_timeout: 60
            
            spelling:
              classname: programy.spelling.norvig.NorvigSpellingChecker
              alphabet: 'abcdefghijklmnopqrstuvwxyz'
              corpus: $BOT_ROOT/corpus.txt
              check_before: true
              check_and_retry: true
              
            conversations:
              type: file
              config_name: file_storage
        
            file_storage:
              dir: $BOT_ROOT/conversations

        """, ConsoleConfiguration(), ".")

        bot_config = BotConfiguration()
        bot_config.load_configuration(yaml, ".")

        self.assertEqual("programy.bot.DefaultBrainSelector", bot_config.brain_selector)

        self.assertEqual("Hi, how can I help you today?", bot_config.initial_question)
        self.assertEqual("YINITIALQUESTION", bot_config.initial_question_srai)
        self.assertEqual("Sorry, I don't have an answer for that!", bot_config.default_response)
        self.assertEqual("YDEFAULTRESPONSE", bot_config.default_response_srai)
        self.assertEqual("So long, and thanks for the fish!", bot_config.exit_response)
        self.assertEqual("YEXITRESPONSE", bot_config.exit_response_srai)
        self.assertEqual("YEMPTY", bot_config.empty_string)
        self.assertEqual(bot_config.max_question_recursion, 1000)
        self.assertEqual(bot_config.max_question_timeout, 60)
        self.assertEqual(bot_config.max_search_depth, 100)
        self.assertEqual(bot_config.max_search_timeout, 60)
        self.assertTrue(bot_config.override_properties)

        self.assertIsNotNone(bot_config.spelling)
        self.assertEqual("programy.spelling.norvig.NorvigSpellingChecker", bot_config.spelling.classname)

        self.assertIsNotNone(bot_config.conversations)
        self.assertEquals(bot_config.conversations.type, "file")
        self.assertIsNotNone(bot_config.conversations.storage)
        self.assertEquals(bot_config.conversations.storage.dir, "./conversations")

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
        """, ConsoleConfiguration(), ".")

        bot_config = BotConfiguration()
        bot_config.load_configuration(yaml, ".")

        self.assertIsNone(bot_config.brain_selector)
        self.assertEqual("Hello", bot_config.initial_question)
        self.assertEqual("", bot_config.initial_question_srai)
        self.assertEqual("", bot_config.default_response)
        self.assertEqual("", bot_config.default_response_srai)
        self.assertEqual("Bye!", bot_config.exit_response)
        self.assertEqual("", bot_config.exit_response_srai)
        self.assertEqual("", bot_config.empty_string)
        self.assertEqual(bot_config.max_question_recursion, 100)
        self.assertEqual(bot_config.max_question_timeout, -1)
        self.assertEqual(bot_config.max_search_depth, 100)
        self.assertEqual(bot_config.max_search_timeout, -1)
        self.assertTrue(bot_config.override_properties)
        self.assertIsNotNone(bot_config.spelling)
        self.assertIsNotNone(bot_config.conversations)

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        with self.assertRaises(Exception):
            yaml.load_from_text("""
            """, ConsoleConfiguration(), ".")
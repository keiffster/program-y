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
              load: true
              classname: programy.spelling.norvig.NorvigSpellingChecker
              alphabet: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
              check_before: true
              check_and_retry: true
              
            splitter:
                classname: programy.dialog.splitter.regex.RegexSentenceSplitter

            joiner:
                classname: programy.dialog.joiner.SentenceJoiner

            conversations:
              save: true
              load: false
              max_histories: 100
              restore_last_topic: false
              initial_topic: TOPIC1
              empty_on_start: false
        
            from_translator:
                classname: programy.nlp.translate.textblob_translator.TextBlobTranslator
                from: fr
                to: en 

            to_translator:
                classname: programy.nlp.translate.textblob_translator.TextBlobTranslator
                from: en
                to: fr

            sentiment:
                classname: programy.nlp.sentiment.textblob_sentiment.TextBlobSentimentAnalyser
                scores: programy.nlp.sentiment.scores.SentimentScores

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
        self.assertEqual(bot_config.spelling.section_name, "spelling")
        self.assertEqual(bot_config.spelling.classname, "programy.spelling.norvig.NorvigSpellingChecker")
        self.assertTrue(bot_config.spelling.check_before)
        self.assertTrue(bot_config.spelling.check_and_retry)

        self.assertIsNotNone(bot_config.splitter)
        self.assertEqual("programy.dialog.splitter.regex.RegexSentenceSplitter", bot_config.splitter.classname)
        self.assertEqual('[:;,.?!]', bot_config.splitter.split_chars)

        self.assertIsNotNone(bot_config.joiner)
        self.assertEqual("programy.dialog.joiner.SentenceJoiner", bot_config.joiner.classname)
        self.assertEqual('.?!', bot_config.joiner.join_chars)

        self.assertIsNotNone(bot_config.conversations)
        self.assertIsNotNone(bot_config.conversations.max_histories, 100)
        self.assertIsNotNone(bot_config.conversations.restore_last_topic, False)
        self.assertIsNotNone(bot_config.conversations.initial_topic, "TOPIC1")
        self.assertIsNotNone(bot_config.conversations.empty_on_start, False)

        self.assertEqual("programy.nlp.translate.textblob_translator.TextBlobTranslator", bot_config.from_translator.classname)
        self.assertEqual("en", bot_config.from_translator.to_lang)
        self.assertEqual("fr", bot_config.from_translator.from_lang)

        self.assertEqual("programy.nlp.translate.textblob_translator.TextBlobTranslator", bot_config.to_translator.classname)
        self.assertEqual("fr", bot_config.to_translator.to_lang)
        self.assertEqual("en", bot_config.to_translator.from_lang)

        self.assertEqual("programy.nlp.sentiment.textblob_sentiment.TextBlobSentimentAnalyser", bot_config.sentiment_analyser.classname)
        self.assertEqual("programy.nlp.sentiment.scores.SentimentScores", bot_config.sentiment_analyser.scores)

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

        self.assertIsNotNone(bot_config.splitter)
        self.assertEqual("programy.dialog.splitter.regex.RegexSentenceSplitter", bot_config.splitter.classname)
        self.assertEqual('[:;,.?!]', bot_config.splitter.split_chars)

        self.assertIsNotNone(bot_config.joiner)
        self.assertEqual("programy.dialog.joiner.joiner.SentenceJoiner", bot_config.joiner.classname)
        self.assertEqual('.?!', bot_config.joiner.join_chars)

        self.assertIsNotNone(bot_config.conversations)

        self.assertIsNotNone(bot_config.from_translator)
        self.assertIsNotNone(bot_config.to_translator)
        self.assertIsNotNone(bot_config.sentiment_analyser)

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        with self.assertRaises(Exception):
            yaml.load_from_text("""
            """, ConsoleConfiguration(), ".")
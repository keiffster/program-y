import unittest
from programy.clients.events.console.config import ConsoleConfiguration
from programy.config.bot.bot import BotConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.utils.license.keys import LicenseKeys
from programytest.config.brain.test_brain import BrainConfigurationTests
from programytest.config.bot.test_conversations import BotConversationsConfigurationTests
from programytest.config.bot.test_joiner import BotSentenceJoinerConfigurationTests
from programytest.config.bot.test_sentiment import BotSentimentAnalyserConfigurationTests
from programytest.config.bot.test_spelling import BotSpellingConfigurationTests
from programytest.config.bot.test_splitter import BotSentenceSplitterConfigurationTests
from programytest.config.bot.test_translate import BotTranslatorConfigurationTests


class BotConfigurationTests(unittest.TestCase):

    def test_getters_and_setters(self):
        bot_config = BotConfiguration()

        bot_config.default_response = "Default response"
        self.assertEquals(bot_config.default_response, "Default response")

        bot_config.default_response_srai = "DEFAULT_RESPONSE"
        self.assertEquals(bot_config.default_response_srai, "DEFAULT_RESPONSE")

        bot_config.empty_string = "Empty String"
        self.assertEquals(bot_config.empty_string, "Empty String")

        bot_config.exit_response = "Exit String"
        self.assertEquals(bot_config.exit_response, "Exit String")

        bot_config.exit_response_srai = "EXITSRAI"
        self.assertEquals(bot_config.exit_response_srai, "EXITSRAI")

        bot_config.initial_question = "EXITSRAI"
        self.assertEquals(bot_config.initial_question, "EXITSRAI")

        bot_config.initial_question_srai = "EXITSRAI"
        self.assertEquals(bot_config.initial_question_srai, "EXITSRAI")

        bot_config.override_properties = True
        self.assertEquals(bot_config.override_properties, True)

    def test_with_data_single_bot(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
          bot_root: .
          default_response: Sorry, I don't have an answer for that!
          default_response_srai: 'YEMPTY'
          exit_response: 'So long, and thanks for the fish!'
          exit_response_srai: 'YEXITRESPONSE'
          initial_question: 'Hi, how can I help you today?'
          initial_question_srai: 'YINITIALQUESTION'
          empty_string: 'YEMPTY'
          override_properties: true
          max_question_recursion: 100
          max_question_timeout: 60
          max_search_depth: 100
          max_search_timeout: 60
          tab_parse_output: true
          spelling:
            classname: programy.spelling.norvig.NorvigSpellingChecker
            alphabet: ABCDEFGHIJKLMNOPQRSTUVWXYZ
            check_before: true
            check_and_retry: true
          conversations:
            max_histories: 100
            restore_last_topic: true
            initial_topic: '*'
            empty_on_start: true
            multi_client: false
          splitter:
            classname: programy.dialog.splitter.regex.RegexSentenceSplitter
            split_chars: '[:;,.?!]'
          joiner:
            classname: programy.dialog.joiner.joiner.SentenceJoiner
            join_chars: .?!
            terminator: .
          from_translator:
            classname: programy.nlp.translate.textblob_translator.TextBlobTranslator
            from: en
            to: fr
          to_translator:
            classname: programy.nlp.translate.textblob_translator.TextBlobTranslator
            from: en
            to: fr
          sentiment:
            classname: programy.nlp.sentiment.textblob_sentiment.TextBlobSentimentAnalyser
            scores: programy.nlp.sentiment.scores.SentimentScores
          brains:
            brain:
              overrides:
                allow_system_aiml: true
                allow_learn_aiml: true
                allow_learnf_aiml: true
              defaults:
                default_get: unknown
                default_property: unknown
                default_map: unknown
              binaries:
                save_binary: true
                load_binary: true
                load_aiml_on_binary_fail: true
              braintree:
                create: true
                save_as_user: system
              security:
                authentication:
                  classname: programy.security.authenticate.passthrough.BasicPassThroughAuthenticationService
                  denied_srai: AUTHENTICATION_FAILED
                  denied_text: Access Denied!
                authorisation:
                  classname: programy.security.authorise.usergroupsauthorisor.BasicUserGroupAuthorisationService
                  denied_srai: AUTHORISATION_FAILED
                  denied_text: Access Denied!
                account_linker:
                  classname: programy.security.linking.accountlinker.BasicAccountLinkerService
                  denied_srai: ACCOUNT_LINKING_FAILED
                  denied_text: Unable to link accounts!
              dynamic:
                sets:
                  NUMBER: programy.dynamic.sets.numeric.IsNumeric
                  ROMAN: programy.dynamic.sets.roman.IsRomanNumeral
                  STOPWORD: programy.dynamic.sets.stopword.IsStopWord
                  SYNSETS: programy.dynamic.sets.synsets.IsSynset
                maps:
                  ROMANTODDEC: programy.dynamic.maps.roman.MapRomanToDecimal
                  DECTOROMAN: programy.dynamic.maps.roman.MapDecimalToRoman
                  LEMMATIZE: programy.dynamic.maps.lemmatize.LemmatizeMap
                  STEMMER: programy.dynamic.maps.stemmer.StemmerMap
                variables:
                  GETTIME: programy.dynamic.variables.datetime.GetTime
              tokenizer:
                classname: programy.dialog.tokenizer.tokenizer.Tokenizer
                split_chars: ' '
              debugfiles:
                save_errors: false
                save_duplicates: false
          brain_selector: programy.brainfactory.DefaultBrainSelector
        """, ConsoleConfiguration(), ".")

        bot_section = yaml.get_section("bot")

        bot_config = BotConfiguration()
        bot_config.load_configuration_section(yaml, bot_section, ".")

        license_keys = LicenseKeys()
        bot_config.check_for_license_keys(license_keys)

        self.assertEqual("Hi, how can I help you today?", bot_config.initial_question)
        self.assertEqual("YINITIALQUESTION", bot_config.initial_question_srai)
        self.assertEqual("Sorry, I don't have an answer for that!", bot_config.default_response)
        self.assertEqual("YEMPTY", bot_config.default_response_srai)
        self.assertEqual("So long, and thanks for the fish!", bot_config.exit_response)
        self.assertEqual("YEXITRESPONSE", bot_config.exit_response_srai)
        self.assertEqual("YEMPTY", bot_config.empty_string)
        self.assertEqual(bot_config.max_question_recursion, 100)
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
        self.assertEqual("programy.dialog.joiner.joiner.SentenceJoiner", bot_config.joiner.classname)
        self.assertEqual('.?!', bot_config.joiner.join_chars)

        self.assertIsNotNone(bot_config.conversations)
        self.assertIsNotNone(bot_config.conversations.max_histories, 100)
        self.assertIsNotNone(bot_config.conversations.restore_last_topic, False)
        self.assertIsNotNone(bot_config.conversations.initial_topic, "TOPIC1")
        self.assertIsNotNone(bot_config.conversations.empty_on_start, False)

        self.assertEqual("programy.nlp.translate.textblob_translator.TextBlobTranslator", bot_config.from_translator.classname)
        self.assertEqual("fr", bot_config.from_translator.to_lang)
        self.assertEqual("en", bot_config.from_translator.from_lang)

        self.assertEqual("programy.nlp.translate.textblob_translator.TextBlobTranslator", bot_config.to_translator.classname)
        self.assertEqual("fr", bot_config.to_translator.to_lang)
        self.assertEqual("en", bot_config.to_translator.from_lang)

        self.assertEqual("programy.nlp.sentiment.textblob_sentiment.TextBlobSentimentAnalyser", bot_config.sentiment_analyser.classname)
        self.assertEqual("programy.nlp.sentiment.scores.SentimentScores", bot_config.sentiment_analyser.scores)

        self.assertEqual("programy.brainfactory.DefaultBrainSelector", bot_config.brain_selector)
        self.assertEqual(1, len(bot_config.configurations))
        BrainConfigurationTests.assert_brain_config(self, bot_config.configurations[0])

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
        """, ConsoleConfiguration(), ".")

        bot_section = yaml.get_section("bot")

        bot_config = BotConfiguration()
        bot_config.load_configuration(yaml, bot_section, ".")

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

        self.assertEqual("programy.brainfactory.DefaultBrainSelector", bot_config.brain_selector)
        self.assertEqual(1, len(bot_config.configurations))

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)

        yaml.load_from_text("""
        other:
        """, ConsoleConfiguration(), ".")

        bot_config = BotConfiguration()
        bot_config.load_configuration(yaml, ".")

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

        self.assertEqual("programy.brainfactory.DefaultBrainSelector", bot_config.brain_selector)
        self.assertEqual(1, len(bot_config.configurations))

    def test_defaults(self):
        bot_config = BotConfiguration()
        data = {}
        bot_config.to_yaml(data, True)

        BotConfigurationTests.assert_defaults(self, data)

    @staticmethod
    def assert_defaults(test, data):
        test.assertEqual(data['bot_root'], ".")
        test.assertEqual(data['default_response'], "")
        test.assertEqual(data['default_response_srai'], "")
        test.assertEqual(data['exit_response'], "Bye!")
        test.assertEqual(data['exit_response_srai'], "")
        test.assertEqual(data['initial_question'], "Hello")
        test.assertEqual(data['initial_question_srai'], "")
        test.assertEqual(data['empty_string'], "")
        test.assertEqual(data['override_properties'], True)
        test.assertEqual(data['max_question_recursion'], 100)
        test.assertEqual(data['max_question_timeout'], -1)
        test.assertEqual(data['max_search_depth'], 100)
        test.assertEqual(data['max_search_timeout'], -1)
        test.assertEqual(data['tab_parse_output'], True)

        test.assertTrue('conversations' in data)
        BotConversationsConfigurationTests.assert_defaults(test, data['conversations'])
        test.assertTrue('spelling' in data)
        BotSpellingConfigurationTests.assert_defaults(test, data['spelling'])
        test.assertTrue('splitter' in data)
        BotSentenceSplitterConfigurationTests.assert_defaults(test, data['splitter'])
        test.assertTrue('joiner' in data)
        BotSentenceJoinerConfigurationTests.assert_defaults(test, data['joiner'])
        test.assertTrue('from_translator' in data)
        BotTranslatorConfigurationTests.assert_defaults(test, data['from_translator'])
        test.assertTrue('to_translator' in data)
        BotTranslatorConfigurationTests.assert_defaults(test, data['to_translator'])
        test.assertTrue('sentiment' in data)
        BotSentimentAnalyserConfigurationTests.assert_defaults(test, data['sentiment'])
        test.assertTrue('brains' in data)
        test.assertTrue('brain' in data['brains'])
        BrainConfigurationTests.assert_defaults(test, data['brains']['brain'])

        test.assertEqual(data['brain_selector'], "programy.brainfactory.DefaultBrainSelector")
        test.assertIsNotNone(data['brains'])
        test.assertEqual(1, len(data['brains']))

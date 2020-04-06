import unittest

from programy.clients.config import ClientConfigurationData
from programy.clients.events.console.config import ConsoleConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile
from programytest.config.bot.test_bot import BotConfigurationTests
from programytest.utils.email.test_config import EmailConfigurationTests
from programytest.triggers.test_config import TriggersConfigurationTests
from programytest.clients.ping.test_config import PingResponderConfigurationTests
from programytest.storage.test_config import StorageConfigurationTests
from programytest.scheduling.test_config import SchedulerConfigurationTests


class ClientConfigurationDataTests(unittest.TestCase):

    def test_with_data_single_bot(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
          prompt: ">>>"
          
          renderer: programy.clients.render.text.TextRenderer
          
          scheduler:
            name: Scheduler1
            debug_level: 0
            add_listeners: True
            remove_all_jobs: True

          bot_selector: programy.clients.botfactory.DefaultBotSelector
          bots:
            bot1:
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
    
                brain_selector: programy.bot.DefaultBrainSelector
                brains:
                    brain1:
                    
                        # Overrides
                        overrides:
                          allow_system_aiml: true
                          allow_learn_aiml: true
                          allow_learnf_aiml: true
                    
                        # Defaults
                        defaults:
                          default_get: unknown
                          default_property: unknown
                          default_map: unknown
                          learnf-path: file
                    
                        # Binary
                        binaries:
                          save_binary: true
                          load_binary: true
                          load_aiml_on_binary_fail: true
                    
                        # Braintree
                        braintree:
                          create: true
                    
                        security:
                            authentication:
                                classname: programy.security.authenticate.passthrough.BasicPassThroughAuthenticationService
                                denied_srai: AUTHENTICATION_FAILED
                            authorisation:
                                classname: programy.security.authorise.usergroupsauthorisor.BasicUserGroupAuthorisationService
                                denied_srai: AUTHORISATION_FAILED
                                usergroups:
                                  storage: file
                    
                        dynamic:
                            variables:
                                gettime: programy.dynamic.variables.datetime.GetTime
                            sets:
                                numeric: programy.dynamic.sets.numeric.IsNumeric
                                roman:   programy.dynamic.sets.roman.IsRomanNumeral
                            maps:
                                romantodec: programy.dynamic.maps.roman.MapRomanToDecimal
                                dectoroman: programy.dynamic.maps.roman.MapDecimalToRoman
                            
        """, ConsoleConfiguration(), ".")

        client_config = ClientConfigurationData("console")
        client_config.load_configuration(yaml, ".")

        self.assertEqual(1, len(client_config.configurations))
        self.assertEqual("programy.clients.botfactory.DefaultBotSelector", client_config.bot_selector)

        self.assertIsNotNone(client_config.scheduler)
        self.assertEqual("Scheduler1", client_config.scheduler.name)
        self.assertEqual(0, client_config.scheduler.debug_level)
        self.assertTrue(client_config.scheduler.add_listeners)
        self.assertTrue(client_config.scheduler.remove_all_jobs)

        self.assertEqual("programy.clients.render.text.TextRenderer", client_config.renderer)

    def test_with_data_multiple_bots(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
          prompt: ">>>"
          
          renderer: programy.clients.render.text.TextRenderer
          
          scheduler:
            name: Scheduler1
            debug_level: 0
            add_listeners: True
            remove_all_jobs: True

          bot_selector: programy.clients.botfactory.DefaultBotSelector
          bots:
            bot1:
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
    
                brain_selector: programy.bot.DefaultBrainSelector
                brains:
                    brain1:
                    
                        # Overrides
                        overrides:
                          allow_system_aiml: true
                          allow_learn_aiml: true
                          allow_learnf_aiml: true
                    
                        # Defaults
                        defaults:
                          default_get: unknown
                          default_property: unknown
                          default_map: unknown
                          learnf-path: file
                    
                        # Binary
                        binaries:
                          save_binary: true
                          load_binary: true
                          load_aiml_on_binary_fail: true
                    
                        # Braintree
                        braintree:
                          create: true
                    
                        security:
                            authentication:
                                classname: programy.security.authenticate.passthrough.BasicPassThroughAuthenticationService
                                denied_srai: AUTHENTICATION_FAILED
                            authorisation:
                                classname: programy.security.authorise.usergroupsauthorisor.BasicUserGroupAuthorisationService
                                denied_srai: AUTHORISATION_FAILED
                                usergroups:
                                  storage: file
                    
                        dynamic:
                            variables:
                                gettime: programy.dynamic.variables.datetime.GetTime
                            sets:
                                numeric: programy.dynamic.sets.numeric.IsNumeric
                                roman:   programy.dynamic.sets.roman.IsRomanNumeral
                            maps:
                                romantodec: programy.dynamic.maps.roman.MapRomanToDecimal
                                dectoroman: programy.dynamic.maps.roman.MapDecimalToRoman

            bot2:
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
    
                brain_selector: programy.bot.DefaultBrainSelector
                brains:
                    brain1:
                    
                        # Overrides
                        overrides:
                          allow_system_aiml: true
                          allow_learn_aiml: true
                          allow_learnf_aiml: true
                    
                        # Defaults
                        defaults:
                          default_get: unknown
                          default_property: unknown
                          default_map: unknown
                          learnf-path: file
                    
                        # Binary
                        binaries:
                          save_binary: true
                          load_binary: true
                          load_aiml_on_binary_fail: true
                    
                        # Braintree
                        braintree:
                          create: true
                    
                        security:
                            authentication:
                                classname: programy.security.authenticate.passthrough.BasicPassThroughAuthenticationService
                                denied_srai: AUTHENTICATION_FAILED
                            authorisation:
                                classname: programy.security.authorise.usergroupsauthorisor.BasicUserGroupAuthorisationService
                                denied_srai: AUTHORISATION_FAILED
                                usergroups:
                                  storage: file
                    
                        dynamic:
                            variables:
                                gettime: programy.dynamic.variables.datetime.GetTime
                            sets:
                                numeric: programy.dynamic.sets.numeric.IsNumeric
                                roman:   programy.dynamic.sets.roman.IsRomanNumeral
                            maps:
                                romantodec: programy.dynamic.maps.roman.MapRomanToDecimal
                                dectoroman: programy.dynamic.maps.roman.MapDecimalToRoman
                            
        """, ConsoleConfiguration(), ".")

        client_config = ClientConfigurationData("console")
        client_config.load_configuration(yaml, ".")

        self.assertEqual(2, len(client_config.configurations))
        self.assertEqual("programy.clients.botfactory.DefaultBotSelector", client_config.bot_selector)

        self.assertIsNotNone(client_config.scheduler)
        self.assertEqual("Scheduler1", client_config.scheduler.name)
        self.assertEqual(0, client_config.scheduler.debug_level)
        self.assertTrue(client_config.scheduler.add_listeners)
        self.assertTrue(client_config.scheduler.remove_all_jobs)

        self.assertEqual("programy.clients.render.text.TextRenderer", client_config.renderer)

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
        """, ConsoleConfiguration(), ".")

        client_config = ClientConfigurationData("console")
        client_config.load_configuration(yaml, ".")

        self.assertIsNotNone(client_config.bot_selector)

        self.assertIsNotNone(client_config.scheduler)
        self.assertEqual(None, client_config.scheduler.name)
        self.assertEqual(0, client_config.scheduler.debug_level)
        self.assertFalse(client_config.scheduler.add_listeners)
        self.assertFalse(client_config.scheduler.remove_all_jobs)

        self.assertIsNotNone(client_config.renderer)

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        other:
        """, ConsoleConfiguration(), ".")

        client_config = ClientConfigurationData("console")
        client_config.load_configuration(yaml, ".")

        self.assertIsNotNone(client_config.bot_selector)

        self.assertIsNotNone(client_config.scheduler)
        self.assertEqual(None, client_config.scheduler.name)
        self.assertEqual(0, client_config.scheduler.debug_level)
        self.assertFalse(client_config.scheduler.add_listeners)
        self.assertFalse(client_config.scheduler.remove_all_jobs)

        self.assertIsNotNone(client_config.renderer)

    def test_defaults(self):
        client_config = ClientConfigurationData("console")
        data = {}
        client_config.to_yaml(data, True)

        ClientConfigurationDataTests.assert_defaults(self, data)

    @staticmethod
    def assert_defaults(test, data):
        test.assertEqual(data['description'], 'ProgramY AIML2.0 Client')
        test.assertEqual(data['renderer'], "programy.clients.render.text.TextRenderer")

        test.assertTrue('scheduler' in data)
        SchedulerConfigurationTests.assert_defaults(test, data['scheduler'])
        test.assertTrue('email' in data)
        EmailConfigurationTests.assert_defaults(test, data['email'])
        test.assertTrue('triggers' in data)
        TriggersConfigurationTests.assert_defaults(test, data['triggers'])
        test.assertTrue('responder' in data)
        PingResponderConfigurationTests.assert_defaults(test, data['responder'])
        test.assertTrue('storage' in data)
        StorageConfigurationTests.assert_defaults(test, data['storage'])
        test.assertTrue('bots' in data)
        test.assertTrue('bot' in data['bots'])
        BotConfigurationTests.assert_defaults(test, data['bots']['bot'])

        test.assertEqual(data['bot_selector'], "programy.clients.botfactory.DefaultBotSelector")

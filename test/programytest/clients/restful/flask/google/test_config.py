import unittest

from programy.clients.events.console.config import ConsoleConfiguration
from programy.clients.restful.flask.google.config import GoogleConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile


class GoogleConfigurationTests(unittest.TestCase):

    def test_init(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        google:
          host: 127.0.0.1
          port: 5000
          debug: false
          launch_text: Hello and welcome
          launch_srai: GOOGLE_LAUNCH
          quit_text: Good bye matey
          quit_srai: GOOGLE_STOP
          help_text: Ask me anything, I know loads
          help_srai: GOOGLE_HELP
          error_text: Oopsie there has been an error
          error_srai: GOOGLE_ERROR
        """, ConsoleConfiguration(), ".")

        google_config = GoogleConfiguration()
        google_config.load_configuration(yaml, ".")

        self.assertEqual("127.0.0.1", google_config.host)
        self.assertEqual(5000, google_config.port)
        self.assertEqual(False, google_config.debug)

        self.assertEqual(google_config.launch_text, "Hello and welcome")
        self.assertEqual(google_config.launch_srai, "GOOGLE_LAUNCH")

        self.assertEqual(google_config.quit_text, "Good bye matey")
        self.assertEqual(google_config.quit_srai, "GOOGLE_STOP")

        self.assertEqual(google_config.help_text, "Ask me anything, I know loads")
        self.assertEqual(google_config.help_srai, "GOOGLE_HELP")

        self.assertEqual(google_config.error_text, "Oopsie there has been an error")
        self.assertEqual(google_config.error_srai, "GOOGLE_ERROR")

    def test_init_no_values(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        google:
        """, ConsoleConfiguration(), ".")

        google_config = GoogleConfiguration()
        google_config.load_configuration(yaml, ".")

        self.assertEqual(google_config.host, "0.0.0.0")
        self.assertEqual(google_config.port, 80)
        self.assertEqual(google_config.debug, False)

        self.assertEqual(google_config.launch_text, "Hello and welcome")
        self.assertEqual(google_config.launch_srai, None)

        self.assertEqual(google_config.quit_text, "Good bye matey")
        self.assertEqual(google_config.quit_srai, None)

        self.assertEqual(google_config.error_text, "Oopsie there has been an error")
        self.assertEqual(google_config.error_srai, None)

    def test_to_yaml_with_defaults(self):
        config = GoogleConfiguration()

        data = {}
        config.to_yaml(data, True)
        self.assertEquals(
            {'launch_text': 'Hello and welcome', 'launch_srai': None, 'quit_text': 'Good bye matey', 'quit_srai': None,
             'help_text': 'Ask me anything, I know loads', 'help_srai': None,
             'error_text': 'Oopsie there has been an error', 'error_srai': None, 'host': '0.0.0.0', 'port': 80,
             'debug': False, 'api': '/api/rest/v1.0/ask', 'use_api_keys': False, 'api_key_file': './api.keys',
             'ssl_cert_file': './rsa.cert', 'ssl_key_file': './rsa.keys', 'authorization': None,
             'description': 'ProgramY AIML2.0 Client', 'bot_selector': 'programy.clients.botfactory.DefaultBotSelector',
             'scheduler': {'name': 'scheduler', 'debug_level': 0, 'add_listeners': False, 'remove_all_jobs': False,
                           'jobstore': {'name': 'mongo', 'mongo': {'collection': 'programy'}},
                           'threadpool': {'max_workers': 20}, 'processpool': {'max_workers': 5},
                           'job_defaults': {'coalesce': False, 'max_instances': 3}},
             'email': {'host': None, 'port': None, 'username': None, 'password': None, 'from_addr': None},
             'triggers': {'manager': 'programy.triggers.local.LocalTriggerManager'},
             'responder': {'name': 'Client Ping Responder', 'host': None, 'port': None, 'ssl_cert_file': None,
                           'ssl_key_file': None, 'url': None, 'shutdown': None, 'register': None, 'unregister': None,
                           'debug': False}, 'renderer': 'programy.clients.render.text.TextRenderer', 'storage': {
                'entities': {'categories': 'file', 'errors': 'file', 'duplicates': 'file', 'learnf': 'file',
                             'conversations': 'file', 'maps': 'file', 'sets': 'file', 'rdf': 'file', 'denormal': 'file',
                             'normal': 'file', 'gender': 'file', 'person': 'file', 'person2': 'file',
                             'regex_templates': 'file', 'properties': 'file', 'defaults': 'file', 'variables': 'file',
                             'twitter': 'file', 'spelling_corpus': 'file', 'license_keys': 'file',
                             'pattern_nodes': 'file', 'template_nodes': 'file', 'binaries': 'file', 'braintree': 'file',
                             'preprocessors': 'file', 'postprocessors': 'file', 'postquestionprocessors': 'file',
                             'usergroups': 'file', 'triggers': 'file'}, 'stores': {'file': {'type': 'file', 'config': {
                    'categories_storage': {'dirs': ['/tmp/categories'], 'extension': 'aiml', 'subdirs': True,
                                           'format': 'xml', 'encoding': 'utf-8', 'delete_on_start': False},
                    'errors_storage': {'file': '/tmp/debug/errors.txt', 'extension': None, 'subdirs': False,
                                       'format': 'text', 'encoding': 'utf-8', 'delete_on_start': False},
                    'duplicates_storage': {'file': '/tmp/debug/duplicates.txt', 'extension': None, 'subdirs': False,
                                           'format': 'text', 'encoding': 'utf-8', 'delete_on_start': False},
                    'learnf_storage': {'dirs': ['/tmp/categories/learnf'], 'extension': 'aiml', 'subdirs': False,
                                       'format': 'xml', 'encoding': 'utf-8', 'delete_on_start': False},
                    'conversation_storage': {'dirs': ['/tmp/conversations'], 'extension': 'txt', 'subdirs': False,
                                             'format': 'text', 'encoding': 'utf-8', 'delete_on_start': False},
                    'sets_storage': {'dirs': ['/tmp/sets'], 'extension': 'txt', 'subdirs': False, 'format': 'text',
                                     'encoding': 'utf-8', 'delete_on_start': False},
                    'maps_storage': {'dirs': ['/tmp/maps'], 'extension': 'txt', 'subdirs': False, 'format': 'text',
                                     'encoding': 'utf-8', 'delete_on_start': False},
                    'rdf_storage': {'dirs': ['/tmp/rdfs'], 'extension': 'txt', 'subdirs': True, 'format': 'text',
                                    'encoding': 'utf-8', 'delete_on_start': False},
                    'denormal_storage': {'file': '/tmp/lookups/denormal.txt', 'extension': None, 'subdirs': False,
                                         'format': 'text', 'encoding': 'utf-8', 'delete_on_start': False},
                    'normal_storage': {'file': '/tmp/lookups/normal.txt', 'extension': None, 'subdirs': False,
                                       'format': 'text', 'encoding': 'utf-8', 'delete_on_start': False},
                    'gender_storage': {'file': '/tmp/lookups/gender.txt', 'extension': None, 'subdirs': False,
                                       'format': 'text', 'encoding': 'utf-8', 'delete_on_start': False},
                    'person_storage': {'file': '/tmp/lookups/person.txt', 'extension': None, 'subdirs': False,
                                       'format': 'text', 'encoding': 'utf-8', 'delete_on_start': False},
                    'person2_storage': {'file': '/tmp/lookups/person2.txt', 'extension': None, 'subdirs': False,
                                        'format': 'text', 'encoding': 'utf-8', 'delete_on_start': False},
                    'regex_storage': {'file': '/tmp/regex/regex-templates.txt', 'extension': None, 'subdirs': False,
                                      'format': 'text', 'encoding': 'utf-8', 'delete_on_start': False},
                    'properties_storage': {'file': '/tmp/properties/properties.txt', 'extension': None,
                                           'subdirs': False, 'format': 'text', 'encoding': 'utf-8',
                                           'delete_on_start': False},
                    'defaults_storage': {'file': '/tmp/properties/defaults.txt', 'extension': None, 'subdirs': False,
                                         'format': 'text', 'encoding': 'utf-8', 'delete_on_start': False},
                    'twitter_storage': {'dirs': ['/tmp/twitter'], 'extension': 'txt', 'subdirs': False,
                                        'format': 'text', 'encoding': 'utf-8', 'delete_on_start': False},
                    'spelling_storage': {'file': '/tmp/spelling/corpus.txt', 'extension': None, 'subdirs': False,
                                         'format': 'text', 'encoding': 'utf-8', 'delete_on_start': False},
                    'license_storage': {'file': '/tmp/licenses/license.keys', 'extension': None, 'subdirs': False,
                                        'format': 'text', 'encoding': 'utf-8', 'delete_on_start': False},
                    'pattern_nodes_storage': {'file': '/tmp/nodes/pattern_nodes.conf', 'extension': None,
                                              'subdirs': False, 'format': 'text', 'encoding': 'utf-8',
                                              'delete_on_start': False},
                    'template_nodes_storage': {'file': '/tmp/nodes/template_nodes.conf', 'extension': None,
                                               'subdirs': False, 'format': 'text', 'encoding': 'utf-8',
                                               'delete_on_start': False},
                    'binaries_storage': {'file': '/tmp/braintree/braintree.bin', 'extension': None, 'subdirs': False,
                                         'format': 'binary', 'encoding': 'utf-8', 'delete_on_start': False},
                    'braintree_storage': {'file': '/tmp/braintree/braintree.xml', 'extension': None, 'subdirs': False,
                                          'format': 'xml', 'encoding': 'utf-8', 'delete_on_start': False},
                    'preprocessors_storage': {'file': '/tmp/processing/preprocessors.conf', 'extension': None,
                                              'subdirs': False, 'format': 'text', 'encoding': 'utf-8',
                                              'delete_on_start': False},
                    'postprocessors_storage': {'file': '/tmp/processing/postprocessors.conf', 'extension': None,
                                               'subdirs': False, 'format': 'text', 'encoding': 'utf-8',
                                               'delete_on_start': False},
                    'postquestionprocessors_storage': {'file': '/tmp/processing/postquestionprocessors.conf',
                                                       'extension': None, 'subdirs': False, 'format': 'text',
                                                       'encoding': 'utf-8', 'delete_on_start': False},
                    'usergroups_storage': {'file': '/tmp/security/usergroups.yaml', 'extension': None, 'subdirs': False,
                                           'format': 'text', 'encoding': 'utf-8', 'delete_on_start': False},
                    'triggers_storage': {'file': '/tmp/triggers/triggers.txt', 'extension': None, 'subdirs': False,
                                         'format': 'text', 'encoding': 'utf-8', 'delete_on_start': False}}}}}, 'bots': {
                'bot': {'bot_root': '.', 'default_response': '', 'default_response_srai': '', 'exit_response': 'Bye!',
                        'exit_response_srai': '', 'initial_question': 'Hello', 'initial_question_srai': '',
                        'empty_string': '', 'override_properties': True, 'max_question_recursion': 100,
                        'max_question_timeout': -1, 'max_search_depth': 100, 'max_search_timeout': -1,
                        'tab_parse_output': True,
                        'spelling': {'classname': 'programy.spelling.norvig.NorvigSpellingChecker',
                                     'alphabet': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'check_before': False,
                                     'check_and_retry': False},
                        'conversations': {'max_histories': 100, 'restore_last_topic': True, 'initial_topic': '*',
                                          'empty_on_start': True, 'multi_client': False},
                        'splitter': {'classname': 'programy.dialog.splitter.regex.RegexSentenceSplitter',
                                     'split_chars': '[:;,.?!]'},
                        'joiner': {'classname': 'programy.dialog.joiner.joiner.SentenceJoiner', 'join_chars': '.?!',
                                   'terminator': '.'}, 'from_translator': {
                        'classname': 'programy.nlp.translate.textblob_translator.TextBlobTranslator', 'from': None,
                        'to': None},
                        'to_translator': {'classname': 'programy.nlp.translate.textblob_translator.TextBlobTranslator',
                                          'from': None, 'to': None}, 'sentiment': {
                        'classname': 'programy.nlp.sentiment.textblob_sentiment.TextBlobSentimentAnalyser',
                        'scores': 'programy.nlp.sentiment.scores.SentimentScores'}, 'brains': {'brain': {
                        'overrides': {'allow_system_aiml': False, 'allow_learn_aiml': False,
                                      'allow_learnf_aiml': False},
                        'defaults': {'default_get': 'unknown', 'default_property': 'unknown', 'default_map': 'unknown'},
                        'binaries': {'save_binary': False, 'load_binary': False, 'load_aiml_on_binary_fail': True},
                        'braintree': {'create': False, 'save_as_user': 'system'}, 'services': {
                            'REST': {'classname': 'programy.services.rest.GenericRESTService', 'method': 'GET',
                                     'host': '0.0.0.0'},
                            'Pannous': {'classname': 'programy.services.pannous.PannousService',
                                        'url': 'http://weannie.pannous.com/api'},
                            'Pandora': {'classname': 'programy.services.pandora.PandoraService',
                                        'url': 'http://www.pandorabots.com/pandora/talk-xml'},
                            'Wikipedia': {'classname': 'programy.services.wikipediaservice.WikipediaService'},
                            'DuckDuckGo': {'classname': 'programy.services.duckduckgo.DuckDuckGoService',
                                           'url': 'http://api.duckduckgo.com'}},
                        'openchatbots': {'openchatbots': {}, 'protocols': ['http'], 'domains': []}, 'security': {
                            'authentication': {
                                'classname': 'programy.security.authenticate.passthrough.BasicPassThroughAuthenticationService',
                                'denied_srai': 'AUTHENTICATION_FAILED', 'denied_text': 'Access Denied!'},
                            'authorisation': {
                                'classname': 'programy.security.authorise.usergroupsauthorisor.BasicUserGroupAuthorisationService',
                                'denied_srai': 'AUTHORISATION_FAILED', 'denied_text': 'Access Denied!'},
                            'account_linker': {
                                'classname': 'programy.security.linking.accountlinker.BasicAccountLinkerService',
                                'denied_srai': 'ACCOUNT_LINKING_FAILED', 'denied_text': 'Unable to link accounts!'}},
                        'oob': {'default': {'classname': 'programy.oob.defaults.default.DefaultOutOfBandProcessor'},
                                'alarm': {'classname': 'programy.oob.defaults.alarm.AlarmOutOfBandProcessor'},
                                'camera': {'classname': 'programy.oob.defaults.camera.CameraOutOfBandProcessor'},
                                'clear': {'classname': 'programy.oob.defaults.clear.ClearOutOfBandProcessor'},
                                'dial': {'classname': 'programy.oob.defaults.dial.DialOutOfBandProcessor'},
                                'dialog': {'classname': 'programy.oob.defaults.dialog.DialogOutOfBandProcessor'},
                                'email': {'classname': 'programy.oob.defaults.email.EmailOutOfBandProcessor'},
                                'geomap': {'classname': 'programy.oob.defaults.map.MapOutOfBandProcessor'},
                                'schedule': {'classname': 'programy.oob.defaults.schedule.ScheduleOutOfBandProcessor'},
                                'search': {'classname': 'programy.oob.defaults.search.SearchOutOfBandProcessor'},
                                'sms': {'classname': 'programy.oob.defaults.sms.SMSOutOfBandProcessor'},
                                'url': {'classname': 'programy.oob.defaults.url.URLOutOfBandProcessor'},
                                'wifi': {'classname': 'programy.oob.defaults.wifi.WifiOutOfBandProcessor'}},
                        'dynamic': {'sets': {'NUMBER': 'programy.dynamic.sets.numeric.IsNumeric',
                                             'ROMAN': 'programy.dynamic.sets.roman.IsRomanNumeral',
                                             'STOPWORD': 'programy.dynamic.sets.stopword.IsStopWord',
                                             'SYNSETS': 'programy.dynamic.sets.synsets.IsSynset'},
                                    'maps': {'ROMANTODDEC': 'programy.dynamic.maps.roman.MapRomanToDecimal',
                                             'DECTOROMAN': 'programy.dynamic.maps.roman.MapDecimalToRoman',
                                             'LEMMATIZE': 'programy.dynamic.maps.lemmatize.LemmatizeMap',
                                             'STEMMER': 'programy.dynamic.maps.stemmer.StemmerMap'},
                                    'variables': {'GETTIME': 'programy.dynamic.variables.datetime.GetTime'}},
                        'tokenizer': {'classname': 'programy.dialog.tokenizer.tokenizer.Tokenizer', 'split_chars': ' '},
                        'debugfiles': {'save_errors': False, 'save_duplicates': False}}},
                        'brain_selector': 'programy.brainfactory.DefaultBrainSelector'}}}

            , data)

    def test_to_yaml_with_no_defaults(self):
        config = GoogleConfiguration()

        data = {}
        config.to_yaml(data, False)

        self.assertEquals(
            {'launch_text': 'Hello and welcome', 'launch_srai': None, 'quit_text': 'Good bye matey', 'quit_srai': None,
             'help_text': 'Ask me anything, I know loads', 'help_srai': None,
             'error_text': 'Oopsie there has been an error', 'error_srai': None, 'host': '0.0.0.0', 'port': 80,
             'debug': False, 'api': '/api/rest/v1.0/ask', 'use_api_keys': False, 'api_key_file': None,
             'ssl_cert_file': None, 'ssl_key_file': None, 'authorization': None,
             'description': 'ProgramY AIML2.0 Client', 'bot_selector': 'programy.clients.botfactory.DefaultBotSelector',
             'scheduler': {'name': None, 'debug_level': 0, 'add_listeners': False, 'remove_all_jobs': False,
                           'jobstore': {'name': None}, 'threadpool': {'max_workers': None},
                           'processpool': {'max_workers': None},
                           'job_defaults': {'coalesce': None, 'max_instances': None}},
             'email': {'host': None, 'port': None, 'username': None, 'password': None, 'from_addr': None},
             'triggers': {'manager': 'programy.triggers.local.LocalTriggerManager'},
             'responder': {'name': 'Client Ping Responder', 'host': None, 'port': None, 'ssl_cert_file': None,
                           'ssl_key_file': None, 'url': None, 'shutdown': None, 'register': None, 'unregister': None,
                           'debug': False}, 'renderer': 'programy.clients.render.text.TextRenderer',
             'storage': {'entities': {}, 'stores': {}}, 'bots': {
                'bot': {'bot_root': '.', 'default_response': '', 'default_response_srai': '', 'exit_response': 'Bye!',
                        'exit_response_srai': '', 'initial_question': 'Hello', 'initial_question_srai': '',
                        'empty_string': '', 'override_properties': True, 'max_question_recursion': 100,
                        'max_question_timeout': -1, 'max_search_depth': 100, 'max_search_timeout': -1,
                        'tab_parse_output': True,
                        'spelling': {'classname': None, 'alphabet': None, 'check_before': False,
                                     'check_and_retry': False},
                        'conversations': {'max_histories': 100, 'restore_last_topic': False, 'initial_topic': '*',
                                          'empty_on_start': False, 'multi_client': False},
                        'splitter': {'classname': 'programy.dialog.splitter.regex.RegexSentenceSplitter',
                                     'split_chars': '[:;,.?!]'},
                        'joiner': {'classname': 'programy.dialog.joiner.joiner.SentenceJoiner', 'join_chars': '.?!',
                                   'terminator': '.'}, 'from_translator': {'classname': None, 'from': None, 'to': None},
                        'to_translator': {'classname': None, 'from': None, 'to': None},
                        'sentiment': {'classname': None, 'scores': None}, 'brains': {'brain': {
                        'overrides': {'allow_system_aiml': False, 'allow_learn_aiml': False,
                                      'allow_learnf_aiml': False},
                        'defaults': {'default_get': 'unknown', 'default_property': 'unknown', 'default_map': 'unknown'},
                        'binaries': {'save_binary': False, 'load_binary': False, 'load_aiml_on_binary_fail': False},
                        'braintree': {'create': False, 'save_as_user': 'system'}, 'services': {},
                        'openchatbots': {'openchatbots': {}, 'protocols': ['http'], 'domains': []}, 'security': {
                            'authentication': {
                                'classname': 'programy.security.authenticate.passthrough.BasicPassThroughAuthenticationService',
                                'denied_srai': 'AUTHENTICATION_FAILED', 'denied_text': 'Access Denied!'},
                            'authorisation': {
                                'classname': 'programy.security.authorise.usergroupsauthorisor.BasicUserGroupAuthorisationService',
                                'denied_srai': 'AUTHORISATION_FAILED', 'denied_text': 'Access Denied!'},
                            'account_linker': {
                                'classname': 'programy.security.linking.accountlinker.BasicAccountLinkerService',
                                'denied_srai': 'ACCOUNT_LINKING_FAILED', 'denied_text': 'Unable to link accounts!'}},
                        'oob': {}, 'dynamic': {'sets': {}, 'maps': {}, 'variables': {}},
                        'tokenizer': {'classname': None, 'split_chars': ' '},
                        'debugfiles': {'save_errors': False, 'save_duplicates': False}}},
                        'brain_selector': 'programy.brainfactory.DefaultBrainSelector'}}}
            , data)

import os

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.clients.events.console.config import ConsoleConfiguration
from programy.utils.substitutions.substitues import Substitutions

from programytest.config.file.base_file_tests import ConfigurationBaseFileTests

class YamlConfigurationFileTests(ConfigurationBaseFileTests):

    def test_get_methods(self):
        config_data = YamlConfigurationFile()
        self.assertIsNotNone(config_data)
        configuration = config_data.load_from_text("""
brain:
    overrides:
      allow_system_aiml: true
      allow_learn_aiml: true
      allow_learnf_aiml: true
          """, ConsoleConfiguration(), ".")
        self.assertIsNotNone(configuration)

        section = config_data.get_section("brainx")
        self.assertIsNone(section)

        section = config_data.get_section("brain")
        self.assertIsNotNone(section)

        child_section = config_data.get_section("overrides", section)
        self.assertIsNotNone(child_section)

        keys = list(config_data.get_child_section_keys("overrides", section))
        self.assertIsNotNone(keys)
        self.assertEqual(3, len(keys))
        self.assertTrue("allow_system_aiml" in keys)
        self.assertTrue("allow_learn_aiml" in keys)
        self.assertTrue("allow_learnf_aiml" in keys)
        self.assertIsNone(config_data.get_child_section_keys("missing", section))
        self.assertEqual(True, config_data.get_option(child_section, "allow_system_aiml"))
        self.assertEqual(True, config_data.get_option(child_section, "missing", missing_value=True))
        self.assertEqual(True, config_data.get_bool_option(child_section, "allow_system_aiml"))
        self.assertEqual(False, config_data.get_bool_option(child_section, "other_value"))
        self.assertEqual(0, config_data.get_int_option(child_section, "other_value"))

    def test_load_from_file(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        configuration = yaml.load_from_file(os.path.dirname(__file__)+ os.sep + "test_yaml.yaml", ConsoleConfiguration(), ".")
        self.assertIsNotNone(configuration)
        self.assert_configuration(configuration)

    def test_load_from_text_multis_one_value(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        configuration = yaml.load_from_text("""
            bot:
                brain:  bot1
        """, ConsoleConfiguration(), ".")
        self.assertIsNotNone(configuration)

        self.assertEqual(1, len(configuration.client_configuration.configurations[0].configurations))

    def test_load_from_text_multis_multiple_values(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        configuration = yaml.load_from_text("""
            console:
                bot: bot
                
            bot:
                brain:  |
                    bot1
                    bot2
        """, ConsoleConfiguration(), ".")
        self.assertIsNotNone(configuration)

        self.assertEqual(2, len(configuration.client_configuration.configurations[0].configurations))

    def test_load_from_text(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        configuration = yaml.load_from_text("""
console:
  bot:  bot
  prompt: ">>>"

  scheduler:
    name: Scheduler1
    debug_level: 50
    add_listeners: False
    remove_all_jobs: False

  storage:
      entities:
          users: sql
          linked_accounts: sql
          links: sql
          properties: file
          conversations:   file
          categories: file
          maps: file
          sets: file
          rdf: file
          denormal: file
          normal: file
          gender: file
          person: file
          person2: file
          twitter: file
          spelling_corpus: file
          license_keys: file
          nodes: file
          binaries: file
          braintree: file
          preprocessors: file
          postprocessors: file
          regex_templates: file
          variables: file
          usergroups: file
          learnf: file

      stores:
          sql:
              type:   sql
              config:
                  url: sqlite:///:memory
                  echo: false
                  encoding: utf-8
                  create_db: true
                  drop_all_first: true

          mongo:
              type:   mongo
              config:
                  url: mongodb://localhost:27017/
                  database: programy
                  drop_all_first: true

          redis:
              type:   redis
              config:
                  host: localhost
                  port: 6379
                  password: null
                  db: 0
                  prefix: programy
                  drop_all_first: True

          file:
              type:   file
              config:
                category_storage:
                  files: ./storage/categories
                conversation_storage:
                  files: ./storage/conversations
                sets_storage:
                  files: ./storage/sets
                  extension: .txt
                  directories: false
                maps_storage:
                  files: ./storage/maps
                  extension: .txt
                  directories: false
                regex_templates:
                  files: ./storage/regex
                lookups_storage:
                  files: ./storage/lookups
                  extension: .txt
                  directories: false
                properties_storage:
                  file: ./storage/properties.txt
                defaults_storage:
                  file: ./storage/defaults.txt
                variables:
                  files: ./storage/variables
                rdf_storage:
                  files: ./storage/rdfs
                  extension: .txt
                  directories: true
                twitter_storage:
                  files: ./storage/twitter
                spelling_corpus:
                  file: ./storage/spelling/corpus.txt
                license_keys:
                  file: ./storage/license.keys
                nodes:
                  files: ./storage/nodes
                binaries:
                  files: ./storage/binaries
                braintree:
                  file: ./storage/braintree/braintree.xml
                  format: xml
                preprocessors:
                  file: ./storage/processing/preprocessors.txt
                postprocessors:
                  file: ./storage/processing/postprocessing.txt
                usergroups:
                  files: ./storage/security/usergroups.txt
                learnf:
                  files: ./storage/categories/learnf

          logger:
              type:   logger
              config:
                  conversation_logger: conversation

voice:
  license_keys: $BOT_ROOT/config/license.keys
  tts: osx
  stt: azhang
  osx:
    classname: talky.clients.voice.tts.osxsay.OSXSayTextToSpeach
  pytts:
    classname: talky.clients.voice.tts.pyttssay.PyTTSSayTextToSpeach
    rate_adjust: 10
  azhang:
    classname: talky.clients.voice.stt.azhang.AnthonyZhangSpeechToText
    ambient_adjust: 3
    service: ibm

rest:
  host: 0.0.0.0
  port: 8989
  debug: false
  workers: 4
  license_keys: $BOT_ROOT/config/license.keys

webchat:
  host: 0.0.0.0
  port: 8090
  debug: false
  license_keys: $BOT_ROOT/config/license.keys
  api: /api/web/v1.0/ask

twitter:
  polling: true
  polling_interval: 49
  streaming: false
  use_status: true
  use_direct_message: true
  auto_follow: true
  storage: file
  welcome_message: Thanks for following me, send me a message and I'll try and help
  license_keys: file

xmpp:
  server: talk.google.com
  port: 5222
  xep_0030: true
  xep_0004: true
  xep_0060: true
  xep_0199: true
  license_keys: file

socket:
  host: 127.0.0.1
  port: 9999
  queue: 5
  debug: true
  license_keys: file

telegram:
  unknown_command: Sorry, that is not a command I have been taught yet!
  license_keys:
  license_keys: file

facebook:
  host: 127.0.0.1
  port: 5000
  debug: false
  license_keys: file

twilio:
  host: 127.0.0.1
  port: 5000
  debug: false
  license_keys: file

slack:
  polling_interval: 1
  license_keys: file

viber:
  name: Servusai
  avatar: http://viber.com/avatar.jpg
  license_keys: file

line:
  host: 127.0.0.1
  port: 8084
  debug: false
  license_keys: file

kik:
  bot_name: servusai
  webhook: https://93638f7a.ngrok.io/api/kik/v1.0/ask
  host: 127.0.0.1
  port: 8082
  debug: false
  license_keys: file

#####################################################################################################
#

bot:
    brain: brain

    initial_question: Hi, how can I help you today?
    initial_question_srai: YINITIALQUESTION
    default_response: Sorry, I don't have an answer for that!
    default_response_srai: YEMPTY
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
      check_before: true
      check_and_retry: true

    conversations:
      max_histories: 100
      restore_last_topic: false
      initial_topic: TOPIC1
      empty_on_start: false

#####################################################################################################
#

brain:

    # Overrides
    overrides:
      allow_system_aiml: true
      allow_learn_aiml: true
      allow_learnf_aiml: true

    # Defaults
    defaults:
      default-get: unknown
      default-property: unknown
      default-map: unknown
      learnf-path: file

    # Binary
    binaries:
      save_binary: true
      load_binary: true
      load_aiml_on_binary_fail: true

    # Braintree
    braintree:
      create: true

    services:
        REST:
            classname: programy.services.rest.GenericRESTService
            method: GET
            host: 0.0.0.0
            port: 8080
        Pannous:
            classname: programy.services.pannous.PannousService
            url: http://weannie.pannous.com/api

    security:
        authentication:
            classname: programy.security.authenticate.passthrough.BasicPassThroughAuthenticationService
            denied_srai: AUTHENTICATION_FAILED
        authorisation:
            classname: programy.security.authorise.usergroupsauthorisor.BasicUserGroupAuthorisationService
            denied_srai: AUTHORISATION_FAILED
            usergroups:
              storage: file

    oob:
      default:
        classname: programy.oob.defaults.default.DefaultOutOfBandProcessor
      alarm:
        classname: programy.oob.defaults.alarm.AlarmOutOfBandProcessor
      camera:
        classname: programy.oob.defaults.camera.CameraOutOfBandProcessor
      clear:
        classname: programy.oob.defaults.clear.ClearOutOfBandProcessor
      dial:
        classname: programy.oob.defaults.dial.DialOutOfBandProcessor
      dialog:
        classname: programy.oob.defaults.dialog.DialogOutOfBandProcessor
      email:
        classname: programy.oob.defaults.email.EmailOutOfBandProcessor
      geomap:
        classname: programy.oob.defaults.map.MapOutOfBandProcessor
      schedule:
        classname: programy.oob.defaults.schedule.ScheduleOutOfBandProcessor
      search:
        classname: programy.oob.defaults.search.SearchOutOfBandProcessor
      sms:
        classname: programy.oob.defaults.sms.SMSOutOfBandProcessor
      url:
        classname: programy.oob.defaults.url.URLOutOfBandProcessor
      wifi:
        classname: programy.oob.defaults.wifi.WifiOutOfBandProcessor

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

        self.assertIsNotNone(configuration)
        self.assert_configuration(configuration)

    def test_load_additionals(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        configuration = yaml.load_from_text("""
            console:
                bot: bot
                
            bot:
                brain: brain
                
            brain:
                services:
                    authentication:
                        classname: programy.services.authenticate.passthrough.PassThroughAuthenticationService
                        denied_srai: ACCESS_DENIED

            """, ConsoleConfiguration(), ".")

        self.assertIsNotNone(configuration)

        self.assertTrue(configuration.client_configuration.configurations[0].configurations[0].services.exists("authentication"))
        auth_service = configuration.client_configuration.configurations[0].configurations[0].services.service("authentication")
        self.assertIsNotNone(auth_service)

        self.assertTrue(auth_service.exists("denied_srai"))
        self.assertEqual("ACCESS_DENIED", auth_service.value("denied_srai"))

    def test_load_with_subs(self):

        subs = Substitutions()
        subs.add_substitute("$ALLOW_SYSTEM", True)

        config_data = YamlConfigurationFile()
        self.assertIsNotNone(config_data)
        configuration = config_data.load_from_text("""
            brain:
                overrides:
                  allow_system_aiml: true
                  allow_learn_aiml: true
                  allow_learnf_aiml: true
          """, ConsoleConfiguration(), ".")
        self.assertIsNotNone(configuration)

        section = config_data.get_section("brainx")
        self.assertIsNone(section)

        section = config_data.get_section("brain")
        self.assertIsNotNone(section)

        child_section = config_data.get_section("overrides", section)
        self.assertIsNotNone(child_section)

        self.assertEqual(True, config_data.get_option(child_section, "allow_system_aiml"))
        self.assertEqual(True, config_data.get_bool_option(child_section, "allow_system_aiml"))
        self.assertEqual(False, config_data.get_bool_option(child_section, "other_value"))

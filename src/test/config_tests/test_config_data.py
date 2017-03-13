import unittest
import os

from programy.config import BaseConfigurationData
from programy.config import BrainFileConfiguration
from programy.config import BrainServiceConfiguration
from programy.config import BrainConfiguration
from programy.config import BotConfiguration
from programy.config import RestConfiguration
from programy.config import ConfigurationFactory
from programy.config import YamlConfigurationFile
from programy.config import JSONConfigurationFile
from programy.config import XMLConfigurationFile
from programy.config import ClientConfiguration
from programy.config import RestClientConfiguration


class LoadConfigurationDataTests(unittest.TestCase):

    def test_load_config_data_yaml(self):
        client_config = ClientConfiguration()
        ConfigurationFactory.load_configuration_from_file(client_config, os.path.dirname(__file__)+"/test_yaml.yaml")
        self.assert_config_data(client_config)

    def test_load_config_data_json(self):
        client_config = ClientConfiguration()
        ConfigurationFactory.load_configuration_from_file(client_config, os.path.dirname(__file__)+"/test_json.json")
        self.assert_config_data(client_config)

    def test_load_config_data_xml(self):
        client_config = ClientConfiguration()
        ConfigurationFactory.load_configuration_from_file(client_config, os.path.dirname(__file__)+"/test_xml.xml")
        self.assert_config_data(client_config)

    def assert_config_data(self, config_data):
        self.assertIsNotNone(config_data)

        self.assertIsNotNone(config_data.bot_configuration)
        self.assertEqual(config_data.bot_configuration.prompt, ">>>")
        self.assertEqual(config_data.bot_configuration.default_response, "Sorry, I don't have an answer for that!")
        self.assertEqual(config_data.bot_configuration.exit_response, "So long, and thanks for the fish!")

        self.assertIsNotNone(config_data.brain_configuration)
        self.assertIsNotNone(config_data.brain_configuration.aiml_files)
        self.assertEqual(config_data.brain_configuration.aiml_files.files, "/aiml")
        self.assertEqual(config_data.brain_configuration.aiml_files.extension, ".aiml")
        self.assertEqual(config_data.brain_configuration.aiml_files.directories, True)

        self.assertIsNotNone(config_data.brain_configuration.set_files)
        self.assertEqual(config_data.brain_configuration.set_files.files, "/sets")
        self.assertEqual(config_data.brain_configuration.set_files.extension, ".txt")
        self.assertEqual(config_data.brain_configuration.set_files.directories, False)

        self.assertIsNotNone(config_data.brain_configuration.map_files)
        self.assertEqual(config_data.brain_configuration.map_files.files, "/maps")
        self.assertEqual(config_data.brain_configuration.map_files.extension, ".txt")
        self.assertEqual(config_data.brain_configuration.map_files.directories, True)

        self.assertEqual(config_data.brain_configuration.denormal, "denormal.txt")
        self.assertEqual(config_data.brain_configuration.normal, "normal.txt")
        self.assertEqual(config_data.brain_configuration.gender, "gender.txt")
        self.assertEqual(config_data.brain_configuration.person2, "person2.txt")
        self.assertEqual(config_data.brain_configuration.predicates, "predicates.txt")
        self.assertEqual(config_data.brain_configuration.pronouns, "pronouns.txt")
        self.assertEqual(config_data.brain_configuration.properties, "properties.txt")
        self.assertEqual(config_data.brain_configuration.triples, "triples.txt")
        self.assertEqual(config_data.brain_configuration.preprocessors, "preprocessors.txt")

        self.assertIsNotNone(config_data.brain_configuration.services)
        self.assertEqual(4, len(config_data.brain_configuration.services))

        self.assertIn(config_data.brain_configuration.services[0].name, ["REST", "PANNOUS", "PANDORA", "WIKIPEDIA"])
        self.assertIn(config_data.brain_configuration.services[0].path, ["programy.utils.services.rest.GenericRESTService",
                                                                         "programy.utils.services.pannous.PannousService",
                                                                         "programy.utils.services.pandora.PandoraService",
                                                                         "programy.utils.services.google.GoogleService",
                                                                         "programy.utils.services.wikipedia.WikipediaService"])

        self.assertIn(config_data.brain_configuration.services[1].name, ["REST", "PANNOUS", "PANDORA", "WIKIPEDIA"])
        self.assertIn(config_data.brain_configuration.services[1].path, ["programy.utils.services.rest.GenericRESTService",
                                                                         "programy.utils.services.pannous.PannousService",
                                                                         "programy.utils.services.pandora.PandoraService",
                                                                         "programy.utils.services.google.GoogleService",
                                                                         "programy.utils.services.wikipedia.WikipediaService"])

        self.assertIn(config_data.brain_configuration.services[2].name, ["REST", "PANNOUS", "PANDORA", "WIKIPEDIA"])
        self.assertIn(config_data.brain_configuration.services[2].path, ["programy.utils.services.rest.GenericRESTService",
                                                                         "programy.utils.services.pannous.PannousService",
                                                                         "programy.utils.services.pandora.PandoraService",
                                                                         "programy.utils.services.google.GoogleService",
                                                                         "programy.utils.services.wikipedia.WikipediaService"])

        self.assertIn(config_data.brain_configuration.services[3].name, ["REST", "PANNOUS", "PANDORA", "WIKIPEDIA"])
        self.assertIn(config_data.brain_configuration.services[3].path, ["programy.utils.services.rest.GenericRESTService",
                                                                         "programy.utils.services.pannous.PannousService",
                                                                         "programy.utils.services.pandora.PandoraService",
                                                                         "programy.utils.services.google.GoogleService",
                                                                         "programy.utils.services.wikipedia.WikipediaService"])


class BaseConfigurationDataTests(unittest.TestCase):

    def test_sub_bot_root(self):
        config = BaseConfigurationData("test")

        replaced = config.sub_bot_root("/data", "/root")
        self.assertIsNotNone(replaced)
        self.assertEqual(replaced, "/data")

        replaced = config.sub_bot_root("$BOT_ROOT/data", "/root")
        self.assertIsNotNone(replaced)
        self.assertEqual(replaced, "/root/data")

        replaced = config.sub_bot_root("$BOT_ROOT$BOT_ROOT/data", "/root")
        self.assertIsNotNone(replaced)
        self.assertEqual(replaced, "/root/root/data")


class BrainFileConfigurationTests(unittest.TestCase):

    def test_init_defaults(self):
        file_config = BrainFileConfiguration(files="/aiml")
        self.assertEqual(file_config.files, "/aiml")
        self.assertEqual(file_config.extension, ".aiml")
        self.assertEqual(file_config.directories, False)

    def test_init(self):
        file_config = BrainFileConfiguration(files="/aiml", extension=".txt", directories=True)
        self.assertEqual(file_config.files, "/aiml")
        self.assertEqual(file_config.extension, ".txt")
        self.assertEqual(file_config.directories, True)


class BrainServiceConfigurationTests(unittest.TestCase):

    def test_init_default(self):
        service_config = BrainServiceConfiguration("Rest")
        self.assertEqual(service_config.name, "REST")
        self.assertEqual(len(service_config.parameters()), 0)

    def test_init(self):
        service_config = BrainServiceConfiguration("REST", {"path": "com.keithsterling.object", "debug": True})
        self.assertEqual(service_config.name, "REST")
        self.assertEqual(len(service_config.parameters()), 2)
        self.assertEqual(service_config.parameter("PATH"), "com.keithsterling.object")
        self.assertEqual(service_config.parameter("DEBUG"), True)
        self.assertEqual(service_config.parameter("XXXX"), None)


class BrainConfigurationTests(unittest.TestCase):

    def test_init(self):
        client_config = ClientConfiguration()
        yaml = YamlConfigurationFile(client_config)
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
          supress_warnings: true
          allow_system_aiml: true
          allow_learn_aiml: true
          allow_learnf_aiml: true

          files:
                aiml:

                    files: $BOT_ROOT/aiml
                    extension: .aiml
                    directories: false
                sets:
                    files: $BOT_ROOT/sets
                    extension: .txt
                    directories: false
                maps:
                    files: $BOT_ROOT/maps
                    extension: .txt
                    directories: false
                denormal: $BOT_ROOT/config/denormal.txt
                normal: $BOT_ROOT/config/normal.txt
                gender: $BOT_ROOT/config/gender.txt
                person: $BOT_ROOT/config/person.txt
                person2: $BOT_ROOT/config/person2.txt
                predicates: $BOT_ROOT/config/predicates.txt
                pronouns: $BOT_ROOT/config/pronouns.txt
                properties: $BOT_ROOT/config/properties.txt
                triples: $BOT_ROOT/config/triples.txt
                preprocessors: $BOT_ROOT/config/preprocessors.conf
                postprocessors: $BOT_ROOT/config/postprocessors.conf

        """, ".")

        brain_config = BrainConfiguration()
        brain_config.load_config_section(yaml, ".")

        self.assertEqual(True, brain_config.supress_warnings)
        self.assertEqual(True, brain_config.allow_system_aiml)
        self.assertEqual(True, brain_config.allow_learn_aiml)
        self.assertEqual(True, brain_config.allow_learnf_aiml)

        self.assertIsNotNone(brain_config.aiml_files)
        self.assertIsNotNone(brain_config.set_files)
        self.assertIsNotNone(brain_config.map_files)
        self.assertEqual("./config/denormal.txt", brain_config.denormal)
        self.assertEqual("./config/normal.txt", brain_config.normal)
        self.assertEqual("./config/gender.txt", brain_config.gender)
        self.assertEqual("./config/person.txt", brain_config.person)
        self.assertEqual("./config/person2.txt", brain_config.person2)
        self.assertEqual("./config/predicates.txt", brain_config.predicates)
        self.assertEqual("./config/pronouns.txt", brain_config.pronouns)
        self.assertEqual("./config/properties.txt", brain_config.properties)
        self.assertEqual("./config/triples.txt", brain_config.triples)
        self.assertEqual("./config/preprocessors.conf", brain_config.preprocessors)
        self.assertEqual("./config/postprocessors.conf", brain_config.postprocessors)
        self.assertIsNotNone(brain_config.services)


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


class RestConfigurationTests(unittest.TestCase):

    def test_init(self):
        client_config = ClientConfiguration()
        yaml = YamlConfigurationFile(client_config)
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        rest:
          host: 127.0.0.1
          port: 5000
          debug: false
          use_api_keys: false
        """, ".")

        rest_config = RestConfiguration()
        rest_config.load_config_section(yaml, ".")

        self.assertEqual("127.0.0.1", rest_config.host)
        self.assertEqual(5000, rest_config.port)
        self.assertEqual(False, rest_config.debug)
        self.assertEqual(False, rest_config.use_api_keys)


class ClientConfigurationTests(unittest.TestCase):

    def test_init(self):
        client_config = ClientConfiguration()
        yaml = YamlConfigurationFile(client_config)
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
          supress_warnings: true
          allow_system_aiml: true
          allow_learn_aiml: true
          allow_learnf_aiml: true

          files:
              aiml:
                  files: /aiml
                  extension: .aiml
                  directories: true
              sets:
                  files: /sets
                  extension: .txt
                  directories: false
              maps:
                  files: /maps
                  extension: .txt
                  directories: true
              denormal: denormal.txt
              normal: normal.txt
              gender: gender.txt
              person: person.txt
              person2: person2.txt
              predicates: predicates.txt
              pronouns: pronouns.txt
              properties: properties.txt
              triples: triples.txt
              preprocessors: preprocessors.txt
              postprocessors: postprocessors.txt

          services:
              REST:
                  path: programy.utils.services.rest.GenericRESTService
              Pannous:
                  path: programy.utils.services.pannous.PannousService
              Pandora:
                  path: programy.utils.services.pandora.PandoraService
              Wikipedia:
                  path: programy.utils.services.wikipedia.WikipediaService

        bot:
          prompt: ">>>"
          default_response: Sorry, I don't have an answer for that!
          exit_response: So long, and thanks for the fish!
          initial_question: Hi, how can I help you?
        """, ".")

        self.assertIsNotNone(client_config.bot_configuration)
        self.assertIsNotNone(client_config.brain_configuration)


class RestClientConfigurationTests(unittest.TestCase):

    def test_init(self):
        client_config = RestClientConfiguration()

        yaml = YamlConfigurationFile(client_config)
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
          supress_warnings: true
          allow_system_aiml: true
          allow_learn_aiml: true
          allow_learnf_aiml: true

          files:
              aiml:
                  files: /aiml
                  extension: .aiml
                  directories: true
              sets:
                  files: /sets
                  extension: .txt
                  directories: false
              maps:
                  files: /maps
                  extension: .txt
                  directories: true
              denormal: denormal.txt
              normal: normal.txt
              gender: gender.txt
              person: person.txt
              person2: person2.txt
              predicates: predicates.txt
              pronouns: pronouns.txt
              properties: properties.txt
              triples: triples.txt
              preprocessors: preprocessors.txt
              postprocessors: postprocessors.txt

          services:
              REST:
                  path: programy.utils.services.rest.GenericRESTService
              Pannous:
                  path: programy.utils.services.pannous.PannousService
              Pandora:
                  path: programy.utils.services.pandora.PandoraService
              Wikipedia:
                  path: programy.utils.services.wikipedia.WikipediaService

        bot:
          prompt: ">>>"
          default_response: Sorry, I don't have an answer for that!
          exit_response: So long, and thanks for the fish!
          initial_question: Hi, how can I help you?

        rest:
          host: 127.0.0.1
          port: 5000
          debug: false
          use_api_keys: false
          """, ".")

        self.assertIsNotNone(client_config.bot_configuration)
        self.assertIsNotNone(client_config.brain_configuration)
        self.assertIsNotNone(client_config.rest_configuration)

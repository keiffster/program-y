import unittest
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.client.client import ClientConfiguration
from programy.config.brain import BrainFileConfiguration

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
                  directories: false
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
          override_predicates: true
        """, ".")

        self.assertIsNotNone(client_config.bot_configuration)
        self.assertIsNotNone(client_config.bot_configuration.prompt)
        self.assertEquals(">>>", client_config.bot_configuration.prompt)
        self.assertIsNotNone(client_config.bot_configuration.default_response)
        self.assertEquals("Sorry, I don't have an answer for that!", client_config.bot_configuration.default_response)
        self.assertIsNotNone(client_config.bot_configuration.exit_response)
        self.assertEquals("So long, and thanks for the fish!", client_config.bot_configuration.exit_response)
        self.assertIsNotNone(client_config.bot_configuration.initial_question)
        self.assertEquals("Hi, how can I help you?", client_config.bot_configuration.initial_question)

        self.assertIsNotNone(client_config.brain_configuration)

        self.assertTrue(client_config.brain_configuration.allow_system_aiml)
        self.assertTrue(client_config.brain_configuration.allow_learn_aiml)
        self.assertTrue(client_config.brain_configuration.allow_learnf_aiml)

        self.assertIsNotNone(client_config.brain_configuration._aiml_files)
        self.assertIsInstance(client_config.brain_configuration._aiml_files, BrainFileConfiguration)
        self.assertEquals("/aiml", client_config.brain_configuration._aiml_files.files)
        self.assertEquals(".aiml", client_config.brain_configuration._aiml_files.extension)
        self.assertTrue(client_config.brain_configuration._aiml_files.directories)

        self.assertIsNotNone(client_config.brain_configuration._set_files)
        self.assertIsInstance(client_config.brain_configuration._set_files, BrainFileConfiguration)
        self.assertEquals("/sets", client_config.brain_configuration._set_files.files)
        self.assertEquals(".txt", client_config.brain_configuration._set_files.extension)
        self.assertFalse(client_config.brain_configuration._set_files.directories)

        self.assertIsNotNone(client_config.brain_configuration._map_files)
        self.assertIsInstance(client_config.brain_configuration._map_files, BrainFileConfiguration)
        self.assertEquals("/maps", client_config.brain_configuration._map_files.files)
        self.assertEquals(".txt", client_config.brain_configuration._map_files.extension)
        self.assertFalse(client_config.brain_configuration._map_files.directories)

        self.assertIsNotNone(client_config.brain_configuration._denormal)
        self.assertEquals("denormal.txt", client_config.brain_configuration._denormal)

        self.assertIsNotNone(client_config.brain_configuration._normal)
        self.assertEquals("normal.txt", client_config.brain_configuration._normal)

        self.assertIsNotNone(client_config.brain_configuration._gender)
        self.assertEquals("gender.txt", client_config.brain_configuration._gender)

        self.assertIsNotNone(client_config.brain_configuration._person)
        self.assertEquals("person.txt", client_config.brain_configuration._person)

        self.assertIsNotNone(client_config.brain_configuration._person2)
        self.assertEquals("person2.txt", client_config.brain_configuration._person2)

        self.assertIsNotNone(client_config.brain_configuration._predicates)
        self.assertEquals("predicates.txt", client_config.brain_configuration._predicates)

        self.assertIsNotNone(client_config.brain_configuration._pronouns)
        self.assertEquals("pronouns.txt", client_config.brain_configuration._pronouns)

        self.assertIsNotNone(client_config.brain_configuration._properties)
        self.assertEquals("properties.txt", client_config.brain_configuration._properties)

        self.assertIsNotNone(client_config.brain_configuration._triples)
        self.assertEquals("triples.txt", client_config.brain_configuration._triples)

        self.assertIsNotNone(client_config.brain_configuration._preprocessors)
        self.assertEquals("preprocessors.txt", client_config.brain_configuration._preprocessors)

        self.assertIsNotNone(client_config.brain_configuration._postprocessors)
        self.assertEquals("postprocessors.txt", client_config.brain_configuration._postprocessors)

        self.assertIsNotNone(client_config.brain_configuration._services)
        self.assertEquals(4, len(client_config.brain_configuration._services))

    def test_init_with_blank_data(self):
        with self.assertRaises(Exception):
            client_config = ClientConfiguration()
            yaml = YamlConfigurationFile(client_config)
            self.assertIsNotNone(yaml)
            yaml.load_from_text("""
            """, ".")

    def test_init_with_empty_sections(self):
        with self.assertRaises(Exception):
            client_config = ClientConfiguration()
            yaml = YamlConfigurationFile(client_config)
            self.assertIsNotNone(yaml)
            yaml.load_from_text("""
        brain:
          files:
            """, ".")

    def test_init_with_files_only(self):
        client_config = ClientConfiguration()
        yaml = YamlConfigurationFile(client_config)
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
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
                  directories: false
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
        bot:
        """, ".")

        self.assertIsNotNone(client_config.bot_configuration)
        self.assertIsNotNone(client_config.bot_configuration.prompt)
        self.assertEquals(">>> ", client_config.bot_configuration.prompt)
        self.assertIsNotNone(client_config.bot_configuration.default_response)
        self.assertEquals("Sorry, I don't have an answer for that right now", client_config.bot_configuration.default_response)
        self.assertIsNotNone(client_config.bot_configuration.exit_response)
        self.assertEquals("Bye!", client_config.bot_configuration.exit_response)
        self.assertIsNotNone(client_config.bot_configuration.initial_question)
        self.assertEquals("Hello", client_config.bot_configuration.initial_question)

        self.assertIsNotNone(client_config.brain_configuration)

        self.assertTrue(client_config.brain_configuration.allow_system_aiml)
        self.assertTrue(client_config.brain_configuration.allow_learn_aiml)
        self.assertTrue(client_config.brain_configuration.allow_learnf_aiml)

        self.assertIsNotNone(client_config.brain_configuration._services)
        self.assertEqual(0, len(client_config.brain_configuration._services))

    def test_init_with_brain_empty_children(self):
        with self.assertRaises(Exception):
            client_config = ClientConfiguration()
            yaml = YamlConfigurationFile(client_config)
            self.assertIsNotNone(yaml)
            yaml.load_from_text("""
            brain:
                files:
                services:
            bot:
            """, ".")


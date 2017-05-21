import unittest
import os

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.client.client import ClientConfiguration

class YamlConfigurationFileTests(unittest.TestCase):



    def test_load_from_file(self):
        client_config = ClientConfiguration()
        yaml = YamlConfigurationFile(client_config)
        self.assertIsNotNone(yaml)
        yaml.load_from_file(os.path.dirname(__file__)+"/test_yaml.yaml", ",")
        self.assertIsNotNone(yaml.yaml_data)
        brain = yaml.get_section("brain")
        self.assertIsNotNone(brain)
        files = yaml.get_section("files", brain)
        self.assertIsNotNone(files)
        aiml = yaml.get_section("aiml", files)
        self.assertIsNotNone(aiml)

        files = yaml.get_section("files", aiml)
        self.assertIsNotNone(files)
        self.assertEqual(files, "/aiml")
        extension = yaml.get_section("extension", aiml)
        self.assertIsNotNone(extension)
        self.assertEqual(extension, ".aiml")
        directories = yaml.get_section("directories", aiml)
        self.assertIsNotNone(directories)
        self.assertEqual(directories, True)

    def test_load_from_text(self):
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

        self.assertIsNotNone(yaml.yaml_data)
        brain = yaml.get_section("brain")
        self.assertIsNotNone(brain)
        files = yaml.get_section("files", brain)
        self.assertIsNotNone(files)
        aiml = yaml.get_section("aiml", files)
        self.assertIsNotNone(aiml)

        files = yaml.get_section("files", aiml)
        self.assertIsNotNone(files)
        self.assertEqual(files, "/aiml")
        extension = yaml.get_section("extension", aiml)
        self.assertIsNotNone(extension)
        self.assertEqual(extension, ".aiml")
        directories = yaml.get_section("directories", aiml)
        self.assertIsNotNone(directories)
        self.assertEqual(directories, True)


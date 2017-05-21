import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.client.client import ClientConfiguration
from programy.config.client.facebook import FacebookConfiguration, FacebookClientConfiguration


class FacebookConfigurationTests(unittest.TestCase):

    def test_init(self):
        client_config = ClientConfiguration()
        yaml = YamlConfigurationFile(client_config)
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
            facebook:
              polling: true
              polling_interval: 30
              streaming: true
        """, ".")

        facebook_config = FacebookConfiguration()
        facebook_config.load_config_section(yaml, ".")

        self.assertTrue(facebook_config.polling)
        self.assertEqual(30, facebook_config.polling_interval)
        self.assertTrue(facebook_config.streaming)


class FacebookClientConfigurationTests(unittest.TestCase):

    def test_init(self):
        client_config = FacebookClientConfiguration()

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

        facebook:
          polling: true
          polling_interval: 30
          streaming: true
          """, ".")

        self.assertIsNotNone(client_config.bot_configuration)
        self.assertIsNotNone(client_config.brain_configuration)
        self.assertIsNotNone(client_config.facebook_configuration)


import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.client.client import ClientConfiguration
from programy.config.client.twitter import TwitterConfiguration, TwitterClientConfiguration

class TwitterConfigurationTests(unittest.TestCase):

    def test_init(self):
        client_config = ClientConfiguration()
        yaml = YamlConfigurationFile(client_config)
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
            twitter:
              polling: true
              polling_interval: 59
              streaming: true
              use_status: true
              use_direct_message: true
              auto_follow: true
              storage: file
              storage_location: ./storage/twitter.data
              welcome_message: Thanks for following me
        """, ".")

        twitter_config = TwitterConfiguration()
        twitter_config.load_config_section(yaml, ".")

        self.assertTrue(twitter_config.polling)
        self.assertEqual(59, twitter_config.polling_interval)
        self.assertTrue(twitter_config.streaming)
        self.assertTrue(twitter_config.use_status)
        self.assertTrue(twitter_config.use_direct_message)
        self.assertTrue(twitter_config.auto_follow)
        self.assertEquals("file", twitter_config.storage)
        self.assertEquals("./storage/twitter.data", twitter_config.storage_location)
        self.assertEquals("Thanks for following me", twitter_config.welcome_message)


class TwitterClientConfigurationTests(unittest.TestCase):

    def test_init(self):
        client_config = TwitterClientConfiguration()

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

        twitter:
          polling: true
          polling_interval: 59
          streaming: true
          use_status: true
          use_direct_message: true
          auto_follow: true
          storage: file
          storage_location: ./storage/twitter.data
          welcome_message: Thanks for following me
          """, ".")

        self.assertIsNotNone(client_config.bot_configuration)
        self.assertIsNotNone(client_config.brain_configuration)
        self.assertIsNotNone(client_config.twitter_configuration)


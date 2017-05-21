import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.client.client import ClientConfiguration
from programy.config.client.xmpp import XmppConfiguration, XmppClientConfiguration


class XmppConfigurationTests(unittest.TestCase):

    def test_init(self):
        client_config = ClientConfiguration()
        yaml = YamlConfigurationFile(client_config)
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
            xmpp:
                server: talk.google.com
                port: 5222
                xep_0030: true
                xep_0004: true
                xep_0060: true
                xep_0199: true
        """, ".")

        xmpp_config = XmppConfiguration()
        xmpp_config.load_config_section(yaml, ".")

        self.assertEquals('talk.google.com', xmpp_config.server)
        self.assertEquals(5222, xmpp_config.port)
        self.assertTrue(xmpp_config.xep_0030)
        self.assertTrue(xmpp_config.xep_0004)
        self.assertTrue(xmpp_config.xep_0060)
        self.assertTrue(xmpp_config.xep_0199)

class XmppClientConfigurationTests(unittest.TestCase):

    def test_init(self):
        client_config = XmppClientConfiguration()

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

        xmpp:
            server: talk.google.com
            port: 5222
            xep_0030: true
            xep_0004: true
            xep_0060: true
            xep_0199: true
          """, ".")

        self.assertIsNotNone(client_config.bot_configuration)
        self.assertIsNotNone(client_config.brain_configuration)
        self.assertIsNotNone(client_config.xmpp_configuration)


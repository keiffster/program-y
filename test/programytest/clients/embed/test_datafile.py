import unittest
import os
from programy.clients.config import ClientConfigurationData
from programy.clients.embed.datafile import EmbeddedDataFileBot
from programy.clients.render.text import TextRenderer


class EmbeddedBotClientTests(unittest.TestCase):

    def test_init(self):
        filepath = os.path.dirname(__file__) + os.sep

        files = {'aiml': [filepath + 'basicbot/categories'],
                 'learnf': [filepath + 'basicbot/learnf'],
                 'patterns': filepath + 'basicbot/nodes/pattern_nodes.conf',
                 'templates': filepath + 'basicbot/nodes/template_nodes.conf',
                 'properties': filepath + 'basicbot/properties/properties.txt',
                 'defaults': filepath + 'basicbot/properties/defaults.txt',
                 'sets': [filepath + 'basicbot/sets'],
                 'maps': [filepath + 'basicbot/maps'],
                 'rdfs': [filepath + 'basicbot/rdfs'],
                 'denormals': filepath + 'basicbot/lookups/denormal.txt',
                 'normals': filepath + 'basicbot/lookups/normal.txt',
                 'genders': filepath + 'basicbot/lookups/gender.txt',
                 'persons': filepath + 'basicbot/lookups/person.txt',
                 'person2s': filepath + 'basicbot/lookups/person2.txt',
                 'regexes': filepath + 'basicbot/regex/regex-templates.txt',
                 'spellings': filepath + 'basicbot/spelling/corpus.txt',
                 'preprocessors': filepath + 'basicbot/processing/preprocessors.conf',
                 'postprocessors': filepath + 'basicbot/processing/postprocessors.conf',
                 'postquestionprocessors': filepath + 'basicbot/processing/postquestionprocessors.conf'
                 }

        client = EmbeddedDataFileBot(files)
        self.assertIsNotNone(client)

        self.assertEqual('ProgramY AIML2.0 Client', client.get_description())
        self.assertIsInstance(client.get_client_configuration(), ClientConfigurationData)

        self.assertFalse(client._render_callback())
        self.assertIsInstance(client.renderer, TextRenderer)

        self.assertNotEqual("", client.ask_question("Hello"))

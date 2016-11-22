import unittest
import xml.etree.ElementTree as ET

from programy.bot import Bot
from programy.brain import Brain
from programy.config import ClientConfiguration, BrainConfiguration
from programy.dialog import Question, Sentence
from programy.parser.template.graph import TemplateGraph
from programy.parser.template.nodes import *


class TemplateGraphSraixTests(unittest.TestCase):

    def setUp(self):
        self.parser = TemplateGraph()
        self.assertIsNotNone(self.parser)

        self.test_brain = None
        self.test_sentence = Sentence("test sentence")
        self.test_sentence._stars = ['one', 'two', 'three', 'four', 'five', 'six']
        self.test_sentence._thatstars = ["*"]
        self.test_sentence._topicstars = ["*"]

        test_config = ClientConfiguration()

        self.test_bot = Bot(Brain(BrainConfiguration()), config=test_config.bot_configuration)
        self.test_clientid = "testid"

        conversation = self.test_bot.get_conversation(self.test_clientid)
        question = Question.create_from_sentence(self.test_sentence)
        conversation._questions.append(question)

    def test_sraix_template_params_as_attribs(self):
        template = ET.fromstring("""
            <template>
                <sraix host="hostname" botid="testbot" hint="test query" apikey="1234567890" service="/ask">
                    Ask this question
                </sraix>
            </template>
            """)
        ast = self.parser.parse_template_expression(template)

    def test_sraix_template_params_as_children(self):
        template = ET.fromstring("""
            <template>
                <sraix>
                    <host>hostname</host>
                    <botid>testbot</botid>
                    <hint>test query</hint>
                    <apikey>1234567890</apikey>
                    <service>/ask</service>
                    Ask this question
                </sraix>
            </template>
            """)
        ast = self.parser.parse_template_expression(template)

if __name__ == '__main__':
    unittest.main()

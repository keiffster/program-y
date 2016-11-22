import unittest
import xml.etree.ElementTree as ET

from programy.bot import Bot
from programy.brain import Brain
from programy.config import ClientConfiguration, BrainConfiguration
from programy.dialog import Question, Sentence
from programy.parser.template.graph import TemplateGraph
from programy.parser.template.nodes import *


class TemplateGraphDateTimeTests(unittest.TestCase):

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

    def test_date_format_as_attrib(self):
        template = ET.fromstring("""
            <template>
                <date format="%c" />
            </template>
            """)
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsNotNone(ast.resolve(self.test_bot, self.test_clientid))

    def test_date_format_as_attrib_full(self):
        template = ET.fromstring("""
            <template>
                <date format="%c"></date>
            </template>
            """)
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsNotNone(ast.resolve(self.test_bot, self.test_clientid))

    def test_date_format_as_attrib_default(self):
        template = ET.fromstring("""
            <template>
                <date/>
            </template>
            """)
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsNotNone(ast.resolve(self.test_bot, self.test_clientid))

    def test_interval_values_as_attribs(self):
        template = ET.fromstring("""
            <template>
                <interval>
                    <format>%c</format>
                    <style>days</style>
                    <from>Wed Oct  5 16:35:11 2016</from>
                    <to>Fri Oct  7 16:35:11 2016</to>
                </interval>
            </template>
            """)
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertEqual(ast.resolve(self.test_bot, self.test_clientid), "2")

if __name__ == '__main__':
    unittest.main()

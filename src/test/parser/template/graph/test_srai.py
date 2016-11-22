import unittest
import xml.etree.ElementTree as ET

from programy.bot import Bot
from programy.brain import Brain
from programy.config import ClientConfiguration, BrainConfiguration
from programy.dialog import Question, Sentence
from programy.parser.template.graph import TemplateGraph
from programy.parser.template.nodes import *


class TemplateGraphSraiTests(unittest.TestCase):

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

    def test_srai_template_simple(self):
        template = ET.fromstring("""
            <template>
                <srai>
                    SRAI this text
                </srai>
            </template>
            """)
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateSRAINode)

        self.assertIsNotNone(ast.children[0].children)
        self.assertEqual(3, len(ast.children[0].children))
        self.assertIsInstance(ast.children[0].children[0], TemplateWordNode)
        self.assertIsInstance(ast.children[0].children[1], TemplateWordNode)
        self.assertIsInstance(ast.children[0].children[2], TemplateWordNode)

    def test_srai_template_nested(self):
        template = ET.fromstring("""
            <template>
                <srai>
                    SRAI This and <srai>SRAI that</srai>
                </srai>
            </template>
            """)
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateSRAINode)

        self.assertIsNotNone(ast.children[0].children)
        self.assertEqual(4, len(ast.children[0].children))
        self.assertIsInstance(ast.children[0].children[0], TemplateWordNode)
        self.assertIsInstance(ast.children[0].children[1], TemplateWordNode)
        self.assertIsInstance(ast.children[0].children[2], TemplateWordNode)
        self.assertIsInstance(ast.children[0].children[3], TemplateSRAINode)

        self.assertIsNotNone(ast.children[0].children[3].children)
        self.assertEqual(2, len(ast.children[0].children[3].children))
        self.assertIsInstance(ast.children[0].children[3].children[0], TemplateWordNode)
        self.assertIsInstance(ast.children[0].children[3].children[1], TemplateWordNode)


if __name__ == '__main__':
    unittest.main()

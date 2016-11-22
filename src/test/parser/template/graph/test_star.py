import unittest
import xml.etree.ElementTree as ET

from programy.bot import Bot
from programy.brain import Brain
from programy.config import ClientConfiguration, BrainConfiguration
from programy.dialog import Question, Sentence
from programy.parser.template.graph import TemplateGraph
from programy.parser.template.nodes import *


class TemplateGraphStarTests(unittest.TestCase):

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

    def test_star_no_index_full(self):
        template = ET.fromstring("""
            <template>
                <star></star>
            </template>
        """)
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsNotNone(ast.children)
        self.assertEqual(1, len(ast.children))
        self.assertIsInstance(ast.children[0], TemplateStarNode)
        self.assertEqual(ast.resolve(self.test_bot, self.test_clientid), "one")

    def test_star_no_index_full_embedded(self):
        template = ET.fromstring("""
            <template>
                Hello <star></star>
            </template>
            """)
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsNotNone(ast.children)
        self.assertEqual(2, len(ast.children))
        self.assertIsInstance(ast.children[0], TemplateWordNode)
        self.assertIsInstance(ast.children[1], TemplateStarNode)
        self.assertEqual(ast.resolve(self.test_bot, self.test_clientid), "Hello one")

    def test_star_no_index_short(self):
        template = ET.fromstring("""
			<template>
				<star />
			</template>
			""")
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsNotNone(ast.children)
        self.assertEqual(1, len(ast.children))
        self.assertIsInstance(ast.children[0], TemplateStarNode)
        self.assertEqual(ast.resolve(self.test_bot, self.test_clientid), "one")

    def test_star_index_as_child(self):
        template = ET.fromstring("""
			<template>
				<star><index>2</index></star>
			</template>
			""")
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsNotNone(ast.children)
        self.assertEqual(1, len(ast.children))
        self.assertIsInstance(ast.children[0], TemplateStarNode)
        self.assertEqual(ast.resolve(self.test_bot, self.test_clientid), "two")

    def test_star_index_as_attrib_full(self):
        template = ET.fromstring("""
			<template>
				<star index="3"></star>
			</template>
			""")
        ast = self.parser.parse_template_expression(template)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast)
        self.assertIsNotNone(ast.children)
        self.assertEqual(1, len(ast.children))
        self.assertIsInstance(ast.children[0], TemplateStarNode)
        self.assertEqual(ast.resolve(self.test_bot, self.test_clientid), "three")

    def test_star_index_as_attrib_short(self):
        template = ET.fromstring("""
			<template>
				<star index="4" />
			</template>
			""")
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsNotNone(ast.children)
        self.assertEqual(1, len(ast.children))
        self.assertIsInstance(ast.children[0], TemplateStarNode)
        self.assertEqual(ast.resolve(self.test_bot, self.test_clientid), "four")

if __name__ == '__main__':
    unittest.main()

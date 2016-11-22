import unittest
import xml.etree.ElementTree as ET

from programy.bot import Bot
from programy.brain import Brain
from programy.config import ClientConfiguration, BrainConfiguration
from programy.dialog import Question, Sentence
from programy.parser.template.graph import TemplateGraph
from programy.parser.template.nodes import *


class TemplateGraphRandomTests(unittest.TestCase):

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

    def test_random_template_no_li(self):
        template = ET.fromstring("""
			<template>
				<random>
				</random>
			</template>
			""")
        with self.assertRaises(ParserException):
            ast = self.parser.parse_template_expression(template)

    def test_random_template(self):
        template = ET.fromstring("""
			<template>
				<random>
					<li>1</li>
					<li>2</li>
					<li>3</li>
				</random>
			</template>
			""")
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateRandomNode)
        self.assertEqual(3, len(ast.children[0].children))

        self.assertIsInstance(ast.children[0].children[0], TemplateNode)
        self.assertIsInstance(ast.children[0].children[1], TemplateNode)
        self.assertIsInstance(ast.children[0].children[2], TemplateNode)

        selection = ast.children[0].resolve(self.test_bot, self.test_clientid)
        self.assertIsNotNone(selection)
        self.assertIn(selection, ['1', '2', '3'])

    def test_random_nested_template(self):
        template = ET.fromstring("""
			<template>
				<random>
					<li>
						<random>
							<li>Say something</li>
							<li>Say the other</li>
						</random>
					</li>
					<li>
						<random>
							<li>Hello world!</li>
							<li>Goodbye cruel world</li>
						</random>
					</li>
				</random>
			</template>
			""")
        ast = self.parser.parse_template_expression(template)

        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateRandomNode)
        self.assertEqual(2, len(ast.children[0].children))

        self.assertIsInstance(ast.children[0].children[0], TemplateNode)
        self.assertEqual(1, len(ast.children[0].children[0].children))
        self.assertIsInstance(ast.children[0].children[0].children[0], TemplateRandomNode)
        self.assertEqual(2, len(ast.children[0].children[0].children[0].children))

        self.assertIsInstance(ast.children[0].children[1], TemplateNode)
        self.assertEqual(1, len(ast.children[0].children[1].children))
        self.assertIsInstance(ast.children[0].children[1].children[0], TemplateRandomNode)
        self.assertEqual(2, len(ast.children[0].children[1].children[0].children))

        selection = ast.children[0].resolve(self.test_bot, self.test_clientid)
        self.assertIsNotNone(selection)
        self.assertIn(selection, ['Say something', 'Say the other', 'Hello world!', 'Goodbye cruel world'])


if __name__ == '__main__':
    unittest.main()

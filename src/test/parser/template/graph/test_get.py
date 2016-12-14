import unittest
import xml.etree.ElementTree as ET

from programy.bot import Bot
from programy.brain import Brain
from programy.config import ClientConfiguration, BrainConfiguration
from programy.dialog import Question, Sentence
from programy.parser.template.graph import TemplateGraph
from programy.parser.template.nodes import *


class TemplateGraphGetTests(unittest.TestCase):

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

    def test_get_template_predicate_as_attrib(self):
        template = ET.fromstring("""
			<template>
				<get name="somepred" />
			</template>
			""")
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        get_node = ast.children[0]
        self.assertIsNotNone(get_node)
        self.assertIsInstance(get_node, TemplateGetNode)
        self.assertIsNotNone(get_node.name)
        self.assertIsInstance(get_node.name, TemplateNode)
        self.assertEqual(get_node.name.resolve(None, None), "somepred")
        self.assertFalse(get_node.local)

    def test_get_template_predicate_as_attrib_mixed(self):
        template = ET.fromstring("""
			<template>
				Hello <get name="somepred" /> how are you
			</template>
			""")
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 5)

        get_node = ast.children[1]
        self.assertIsNotNone(get_node)
        self.assertIsInstance(get_node, TemplateGetNode)
        self.assertIsNotNone(get_node.name)
        self.assertIsInstance(get_node.name, TemplateNode)
        self.assertEqual(get_node.name.resolve(None, None), "somepred")
        self.assertFalse(get_node.local)

    def test_get_template_var_as_attrib(self):
        template = ET.fromstring("""
			<template>
				<get var="somevar" />
			</template>
			""")
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        get_node = ast.children[0]
        self.assertIsNotNone(get_node)
        self.assertIsInstance(get_node, TemplateGetNode)
        self.assertIsNotNone(get_node.name)
        self.assertIsInstance(get_node.name, TemplateNode)
        self.assertEqual(get_node.name.resolve(None, None), "somevar")
        self.assertTrue(get_node.local)

    def test_get_template_predicate_as_child(self):
        template = ET.fromstring("""
			<template>
				<get><name>somepred as text</name></get>
			</template>
			""")
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        get_node = ast.children[0]
        self.assertIsNotNone(get_node)
        self.assertIsInstance(get_node, TemplateGetNode)
        self.assertIsNotNone(get_node.name)
        self.assertIsInstance(get_node.name, TemplateNode)
        self.assertEqual(get_node.name.resolve(None, None), "somepred as text")
        self.assertFalse(get_node.local)

    def test_get_template_local_as_child(self):
        template = ET.fromstring("""
			<template>
				<get><var>somevar</var></get>
			</template>
			""")
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        get_node = ast.children[0]
        self.assertIsNotNone(get_node)
        self.assertIsInstance(get_node, TemplateGetNode)
        self.assertIsNotNone(get_node.name)
        self.assertIsInstance(get_node.name, TemplateNode)
        self.assertEqual(get_node.name.resolve(None, None), "somevar")
        self.assertTrue(get_node.local)

if __name__ == '__main__':
    unittest.main()

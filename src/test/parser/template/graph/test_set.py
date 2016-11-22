import unittest
import xml.etree.ElementTree as ET

from programy.bot import Bot
from programy.brain import Brain
from programy.config import ClientConfiguration, BrainConfiguration
from programy.dialog import Question, Sentence
from programy.parser.template.graph import TemplateGraph
from programy.parser.template.nodes import *


class TemplateGraphSetTests(unittest.TestCase):

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

    def test_set_template_predicate_as_attrib(self):
        template = ET.fromstring("""
			<template>
				<set name="somepred">Value1</set>
			</template>
			""")
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        set_node = ast.children[0]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateSetNode)
        self.assertIsNotNone(set_node.name)
        self.assertIsInstance(set_node.name, TemplateNode)
        self.assertEqual(set_node.name.resolve(None, None), "somepred")
        self.assertFalse(set_node.local)

        self.assertEqual(len(set_node.children), 1)
        self.assertEqual(set_node.children[0].resolve(None, None), "Value1")

    def test_set_template_multi_word_predicate_as_attrib(self):
        template = ET.fromstring("""
            <template>
                <set name="somepred other">Value1</set>
            </template>
            """)
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        set_node = ast.children[0]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateSetNode)
        self.assertIsNotNone(set_node.name)
        self.assertIsInstance(set_node.name, TemplateNode)
        self.assertEqual(set_node.name.resolve(None, None), "somepred other")
        self.assertFalse(set_node.local)

        self.assertEqual(len(set_node.children), 1)
        self.assertEqual(set_node.children[0].resolve(None, None), "Value1")

    def test_set_template_predicate_nested(self):
        template = ET.fromstring("""
			<template>
				Some text here
				<set name="somepred">Value1</set>
				Some text there
			</template>
			""")
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 7)

        set_node = ast.children[3]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateSetNode)
        self.assertIsNotNone(set_node.name)
        self.assertIsInstance(set_node.name, TemplateNode)
        self.assertEqual(set_node.name.resolve(None, None), "somepred")
        self.assertFalse(set_node.local)

        self.assertEqual(len(set_node.children), 1)
        self.assertEqual(set_node.children[0].resolve(None, None), "Value1")

    def test_set_template_local_as_attrib(self):
        template = ET.fromstring("""
			<template>
				<set var="somevar">Value2</set>
			</template>
			""")
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        set_node = ast.children[0]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateSetNode)
        self.assertIsNotNone(set_node.name)
        self.assertIsInstance(set_node.name, TemplateNode)
        self.assertEqual(set_node.name.resolve(None, None), "somevar")
        self.assertTrue(set_node.local)

        self.assertEqual(len(set_node.children), 1)
        self.assertEqual(set_node.children[0].resolve(None, None), "Value2")

    def test_set_template_predicate_as_child(self):
        template = ET.fromstring("""
			<template>
				<set><name>somepred</name>Value3</set>
			</template>
			""")
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        set_node = ast.children[0]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateSetNode)
        self.assertIsNotNone(set_node.name)
        self.assertIsInstance(set_node.name, TemplateNode)
        self.assertEqual(set_node.name.resolve(None, None), "somepred")
        self.assertFalse(set_node.local)

        self.assertEqual(len(set_node.children), 1)
        self.assertEqual(set_node.children[0].resolve(None, None), "Value3")

    def test_set_template_local_as_child(self):
        template = ET.fromstring("""
			<template>
				<set><var>somepred</var>Value4</set>
			</template>
			""")
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        set_node = ast.children[0]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateSetNode)
        self.assertIsNotNone(set_node.name)
        self.assertIsInstance(set_node.name, TemplateNode)
        self.assertEqual(set_node.name.resolve(None, None), "somepred")
        self.assertTrue(set_node.local)

        self.assertEqual(len(set_node.children), 1)
        self.assertEqual(set_node.children[0].resolve(None, None), "Value4")


if __name__ == '__main__':
    unittest.main()

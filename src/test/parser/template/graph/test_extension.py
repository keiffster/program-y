import unittest
import xml.etree.ElementTree as ET

from programy.bot import Bot
from programy.brain import Brain
from programy.config import ClientConfiguration, BrainConfiguration
from programy.dialog import Question, Sentence
from programy.parser.template.graph import TemplateGraph
from programy.parser.template.nodes import *

class TestExtension(object):

    def execute(self, data):
        return "executed"

class TemplateGraphBotTests(unittest.TestCase):

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

    def test_extension_as_attrib(self):
        template = ET.fromstring("""
			<template>
				<extension path="test.parser.template.graph.test_extension.TestExtension">
				1 2 3
				</extension>
			</template>
			""")
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        ext_node = ast.children[0]
        self.assertIsNotNone(ext_node)
        self.assertIsInstance(ext_node, TemplateExtensionNode)
        self.assertIsNotNone(ext_node._path)

        self.assertEqual(len(ext_node.children), 3)
        self.assertEqual("executed", ext_node.resolve(None, None))

    def test_extension_as_child(self):
        template = ET.fromstring("""
            <template>
                <extension>
                    <path>test.parser.template.graph.test_extension.TestExtension</path>
                    1 2 3
                </extension>
            </template>
            """)
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        ext_node = ast.children[0]
        self.assertIsNotNone(ext_node)
        self.assertIsInstance(ext_node, TemplateExtensionNode)
        self.assertIsNotNone(ext_node._path)

        self.assertEqual(len(ext_node.children), 3)
        self.assertEqual("executed", ext_node.resolve(None, None))

if __name__ == '__main__':
    unittest.main()

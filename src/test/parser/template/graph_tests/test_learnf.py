import unittest
import xml.etree.ElementTree as ET

from programy.config.brain import BrainFileConfiguration

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.learn import LearnCategory
from programy.parser.template.nodes.learnf import TemplateLearnfNode

from test.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphLearnfTests(TemplateGraphTestClient):

     def test_learnf_simple(self):
        template = ET.fromstring("""
			<template>
				<learnf>
				    <category>
				        <pattern>HELLO <eval>WORLD</eval> THERE</pattern>
				        <template>HIYA</template>
				    </category>
				</learnf>
			</template>
			""")

        self.test_bot.brain._configuration._aiml_files = BrainFileConfiguration("/tmp", ".aiml", False)

        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        learn_node = ast.children[0]
        self.assertIsNotNone(learn_node)
        self.assertIsInstance(learn_node, TemplateLearnfNode)
        self.assertEqual(1, len(learn_node.children))
        self.assertIsInstance(learn_node.children[0], LearnCategory)
        self.assertIsNotNone(learn_node.children[0].pattern)
        self.assertIsInstance(learn_node.children[0].pattern, ET.Element)
        self.assertIsNotNone(learn_node.children[0].topic)
        self.assertIsInstance(learn_node.children[0].topic, ET.Element)
        self.assertIsNotNone(learn_node.children[0].that)
        self.assertIsInstance(learn_node.children[0].that, ET.Element)
        self.assertIsNotNone(learn_node.children[0].template)
        self.assertIsInstance(learn_node.children[0].template, TemplateNode)

        resolved = learn_node.resolve(self.test_bot, self.test_clientid)
        self.assertEqual(resolved, "")

        response = self.test_bot.ask_question(self.test_clientid, "HELLO WORLD THERE")
        self.assertEqual("HIYA", response)

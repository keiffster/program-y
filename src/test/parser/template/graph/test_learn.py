import unittest
import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.eval import TemplateEvalNode
from programy.parser.template.nodes.learn import TemplateLearnNode
from programy.parser.template.nodes.word import TemplateWordNode


from programy.config.brain import BrainFileConfiguration
from test.parser.template.graph.test_graph_client import TemplateGraphTestClient


class TemplateGraphLearnTests(TemplateGraphTestClient):

     def test_eval_simple(self):
        template = ET.fromstring("""
			<template>
				<eval>sometext</eval>
			</template>
			""")

        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        eval_node = ast.children[0]
        self.assertIsNotNone(eval_node)
        self.assertIsInstance(eval_node, TemplateEvalNode)

        self.assertIsNotNone(eval_node.children)
        self.assertEqual(len(eval_node.children), 1)
        self.assertIsInstance(eval_node.children[0], TemplateWordNode)

        self.assertEqual(eval_node.resolve(self.test_bot, self.test_clientid), "sometext")

     def test_learn_simple(self):

        template = ET.fromstring("""
			<template>
				<learn>
				    <category>
				        <pattern>HELLO <eval>WORLD</eval> THERE</pattern>
				        <template>HIYA</template>
				    </category>
				</learn>
			</template>
			""")

        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        learn_node = ast.children[0]
        self.assertIsNotNone(learn_node)
        self.assertIsInstance(learn_node, TemplateLearnNode)
        self.assertIsNotNone(learn_node._pattern)
        self.assertIsInstance(learn_node._pattern, ET.Element)
        self.assertIsNotNone(learn_node._topic)
        self.assertIsInstance(learn_node._topic, ET.Element)
        self.assertIsNotNone(learn_node._that)
        self.assertIsInstance(learn_node._that, ET.Element)
        self.assertIsNotNone(learn_node._template)
        self.assertIsInstance(learn_node._template, TemplateNode)

        resolved = learn_node.resolve(self.test_bot, self.test_clientid)
        self.assertEqual(resolved, "")

        response = self.test_bot.ask_question(self.test_clientid, "HELLO WORLD THERE")
        self.assertEqual("HIYA", response)

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
        self.assertIsInstance(learn_node, TemplateLearnNode)
        self.assertIsNotNone(learn_node._pattern)
        self.assertIsInstance(learn_node._pattern, ET.Element)
        self.assertIsNotNone(learn_node._topic)
        self.assertIsInstance(learn_node._topic, ET.Element)
        self.assertIsNotNone(learn_node._that)
        self.assertIsInstance(learn_node._that, ET.Element)
        self.assertIsNotNone(learn_node._template)
        self.assertIsInstance(learn_node._template, TemplateNode)

        resolved = learn_node.resolve(self.test_bot, self.test_clientid)
        self.assertEqual(resolved, "")

        response = self.test_bot.ask_question(self.test_clientid, "HELLO WORLD THERE")
        self.assertEqual("HIYA", response)

if __name__ == '__main__':
    unittest.main()

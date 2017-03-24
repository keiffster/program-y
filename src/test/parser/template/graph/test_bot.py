import xml.etree.ElementTree as ET

import unittest

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.bot import TemplateBotNode

from test.parser.template.graph.test_graph_client import TemplateGraphTestClient


class TemplateGraphBotTests(TemplateGraphTestClient):

    def test_bot_name_as_attrib(self):
        template = ET.fromstring("""
			<template>
				<bot name="somebot">sometext</bot>
			</template>
			""")
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        set_node = ast.children[0]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateBotNode)
        self.assertIsNotNone(set_node.name)
        self.assertIsInstance(set_node.name, TemplateNode)
        self.assertEqual(set_node.name.resolve(None, None), "somebot")

        self.assertEqual(len(set_node.children), 1)
        self.assertEqual(set_node.children[0].resolve(None, None), "sometext")

    def test_bot_name_as_child(self):
        template = ET.fromstring("""
			<template>
				<bot><name>somebot</name>sometext</bot>
			</template>
			""")
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        set_node = ast.children[0]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateBotNode)
        self.assertIsNotNone(set_node.name)
        self.assertIsInstance(set_node.name, TemplateNode)
        self.assertEqual(set_node.name.resolve(None, None), "somebot")

        self.assertEqual(len(set_node.children), 1)
        self.assertEqual(set_node.children[0].resolve(None, None), "sometext")

if __name__ == '__main__':
    unittest.main()

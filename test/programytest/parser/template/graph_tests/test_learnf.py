import xml.etree.ElementTree as ET

import os

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.learn import LearnCategory
from programy.parser.template.nodes.learnf import TemplateLearnfNode

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


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

        ast = self._graph.parse_template_expression(template)
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

        resolved = learn_node.resolve(self._client_context)
        self.assertEqual(resolved, "")

        response = self._client_context.bot.ask_question(self._client_context, "HELLO WORLD THERE")
        self.assertEqual("HIYA.", response)

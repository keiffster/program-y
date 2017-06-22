import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.interval import TemplateIntervalNode

from test.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphIntervalTests(TemplateGraphTestClient):

    def test_denormize_node_from_xml(self):
        template = ET.fromstring("""
			<template>
				<interval>Text</interval>
			</template>
			""")
        root = self.parser.parse_template_expression(template)
        self.assertIsNotNone(root)
        self.assertIsInstance(root, TemplateNode)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 1)

        node = root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, TemplateIntervalNode)

    def test_interval_values_as_attribs(self):
        template = ET.fromstring("""
            <template>
                <interval>
                    <format>%c</format>
                    <style>days</style>
                    <from>Wed Oct  5 16:35:11 2016</from>
                    <to>Fri Oct  7 16:35:11 2016</to>
                </interval>
            </template>
            """)
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        set_node = ast.children[0]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateIntervalNode)
        self.assertEqual(ast.resolve(self.test_bot, self.test_clientid), "2")


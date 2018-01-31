import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.program import TemplateProgramNode
from programy.parser.exceptions import ParserException

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphProgramTests(TemplateGraphTestClient):

    def test_program_node_from_xml(self):
        template = ET.fromstring("""
			<template>
				<program />
			</template>
			""")
        root = self._graph.parse_template_expression(template)
        self.assertIsNotNone(root)
        self.assertIsInstance(root, TemplateNode)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 1)

        node = root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, TemplateProgramNode)

    def test_program_with_childrenl(self):
        template = ET.fromstring("""
			<template>
				<program>Text</program>
			</template>
			""")
        with self.assertRaises(ParserException):
            root = self._graph.parse_template_expression(template)

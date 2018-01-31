import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.id import TemplateIdNode
from programy.parser.exceptions import ParserException

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphIdTests(TemplateGraphTestClient):

    def test_id_shorthand_node_from_xml(self):
        template = ET.fromstring("""
			<template>
				<id />
			</template>
			""")
        root = self._graph.parse_template_expression(template)
        self.assertIsNotNone(root)
        self.assertIsInstance(root, TemplateNode)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 1)

        node = root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, TemplateIdNode)

    def test_id_node_from_xml(self):
        template = ET.fromstring("""
			<template>
				<id></id>
			</template>
			""")
        root = self._graph.parse_template_expression(template)
        self.assertIsNotNone(root)
        self.assertIsInstance(root, TemplateNode)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 1)

        node = root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, TemplateIdNode)

    def test_id_with_children(self):
        template = ET.fromstring("""
        			<template>
        				<id>Error</id>
        			</template>
        			""")
        with self.assertRaises(ParserException):
            root = self._graph.parse_template_expression(template)

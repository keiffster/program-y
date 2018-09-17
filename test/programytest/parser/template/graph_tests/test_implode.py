import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.implode import TemplateImplodeNode
from programy.parser.template.nodes.star import TemplateStarNode

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphImplodeTests(TemplateGraphTestClient):

    def test_implode_node_from_xml(self):
        template = ET.fromstring("""
			<template>
				<implode>Text</implode>
			</template>
			""")
        root = self._graph.parse_template_expression(template)
        self.assertIsNotNone(root)
        self.assertIsInstance(root, TemplateNode)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 1)

        node = root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, TemplateImplodeNode)

    def test_implode_node_from_xml_default_to_star(self):
        template = ET.fromstring("""
			<template>
				<implode />
			</template>
			""")
        root = self._graph.parse_template_expression(template)
        self.assertIsNotNone(root)
        self.assertIsInstance(root, TemplateNode)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 1)

        gender_node = root.children[0]
        self.assertIsNotNone(gender_node)
        self.assertIsInstance(gender_node, TemplateImplodeNode)

        self.assertEqual(1, len(gender_node.children))
        next_node = gender_node.children[0]
        self.assertIsInstance(next_node, TemplateStarNode)

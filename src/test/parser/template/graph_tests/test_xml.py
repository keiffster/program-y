import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.xml import TemplateXMLNode

from test.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphXMLTests(TemplateGraphTestClient):

    def test_basic_xml_node_from_xml(self):
        template = ET.fromstring("""
			<template>
				<dial>07777777</dial>
			</template>
			""")
        root = self.parser.parse_template_expression(template)
        self.assertIsNotNone(root)
        self.assertIsInstance(root, TemplateNode)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 1)

        node = root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, TemplateXMLNode)

    def test_attrib_xml_node_from_xml(self):
        template = ET.fromstring("""
			<template>
				<dial leave_message="true">07777777</dial>
			</template>
			""")
        root = self.parser.parse_template_expression(template)
        self.assertIsNotNone(root)
        self.assertIsInstance(root, TemplateNode)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 1)

        node = root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, TemplateXMLNode)

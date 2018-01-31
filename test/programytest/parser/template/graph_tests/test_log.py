import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.log import TemplateLogNode

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphLogTests(TemplateGraphTestClient):

    def test_log_node_from_xml_default_values(self):
        template = ET.fromstring("""
			<template>
				<log>Text</log>
			</template>
			""")
        root = self._graph.parse_template_expression(template)
        self.assertIsNotNone(root)
        self.assertIsInstance(root, TemplateNode)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 1)

        node = root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, TemplateLogNode)

    def test_log_node_from_xml_logging(self):
        template = ET.fromstring("""
			<template>
				<log output="logging">Text</log>
			</template>
			""")
        root = self._graph.parse_template_expression(template)
        self.assertIsNotNone(root)
        self.assertIsInstance(root, TemplateNode)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 1)

        node = root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, TemplateLogNode)

        def test_log_node_from_xml_logging_level(self):
            template = ET.fromstring("""
    			<template>
    				<log output="logging" level="debug>Text</log>
    			</template>
    			""")
            root = self._graph.parse_template_expression(template)
            self.assertIsNotNone(root)
            self.assertIsInstance(root, TemplateNode)
            self.assertIsNotNone(root.children)
            self.assertEqual(len(root.children), 1)

            node = root.children[0]
            self.assertIsNotNone(node)
            self.assertIsInstance(node, TemplateLogNode)

    def test_log_node_from_xml_print(self):
        template = ET.fromstring("""
			<template>
				<log output="print">Text</log>
			</template>
			""")
        root = self._graph.parse_template_expression(template)
        self.assertIsNotNone(root)
        self.assertIsInstance(root, TemplateNode)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 1)

        node = root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, TemplateLogNode)

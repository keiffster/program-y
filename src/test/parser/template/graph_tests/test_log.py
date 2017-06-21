import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.log import TemplateLogNode

from test.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphLogTests(TemplateGraphTestClient):

    def test_log_node_from_xml(self):
        template = ET.fromstring("""
			<template>
				<log>Text</log>
			</template>
			""")
        root = self.parser.parse_template_expression(template)
        self.assertIsNotNone(root)
        self.assertIsInstance(root, TemplateNode)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 1)

        node = root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, TemplateLogNode)

import unittest
import xml.etree.ElementTree as ET

from programy.parser.template.nodes.sr import TemplateSrNode

from test.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphSrTests(TemplateGraphTestClient):

    def test_size(self):
        template = ET.fromstring("""
			<template>
				<sr />
			</template>
			""")
        root = self.parser.parse_template_expression(template)
        self.assertIsNotNone(root)
        node = root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, TemplateSrNode)


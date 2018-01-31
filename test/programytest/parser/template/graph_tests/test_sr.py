import xml.etree.ElementTree as ET

from programy.parser.template.nodes.sr import TemplateSrNode
from programy.parser.exceptions import ParserException

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphSrTests(TemplateGraphTestClient):

    def test_size(self):
        template = ET.fromstring("""
			<template>
				<sr />
			</template>
			""")
        root = self._graph.parse_template_expression(template)
        self.assertIsNotNone(root)
        node = root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, TemplateSrNode)

    def test_size_with_children(self):
        template = ET.fromstring("""
			<template>
				<sr>Something</sr>
			</template>
			""")
        with self.assertRaises(ParserException):
            root = self._graph.parse_template_expression(template)

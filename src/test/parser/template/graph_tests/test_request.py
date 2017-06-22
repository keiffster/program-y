import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.request import TemplateRequestNode

from test.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphRequestTests(TemplateGraphTestClient):

    def test_request_index_as_attrib_full(self):
        template = ET.fromstring("""
			<template>
				<request index="8"></request>
			</template>
			""")
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        set_node = ast.children[0]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateRequestNode)


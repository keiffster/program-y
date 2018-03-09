import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient

class TemplateGraphBasicTests(TemplateGraphTestClient):

    def test_template_no_content(self):
        template = ET.fromstring("""
			<template>
			</template>
			""")
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertEqual(0, len(ast.children))
        self.assertEqual("", ast.resolve(self._client_context))


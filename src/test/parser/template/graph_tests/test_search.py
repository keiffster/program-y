import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.search import TemplateSearchNode

from test.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient

class TemplateGraphSearchTests(TemplateGraphTestClient):

     def test_search_basic(self):
        template = ET.fromstring("""
			<template>
			    <search>
			        question
			    </search>
			</template>
			""")

        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateSearchNode)
        self.assertEqual(1, len(ast.children[0].children))


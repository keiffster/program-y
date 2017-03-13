import unittest
import xml.etree.ElementTree as ET

from programy.parser.template.nodes import *
from test.parser.template.graph.test_graph_client import TemplateGraphTestClient

class TemplateGraphBasicTests(TemplateGraphTestClient):

    def test_template_no_content(self):
        template = ET.fromstring("""
			<template>
			</template>
			""")
        with self.assertRaises(ParserException):
            ast = self.parser.parse_template_expression(template)

    def test_base_template(self):
        template = ET.fromstring("""
			<template>HELLO WORLD</template>
			""")
        ast = self.parser.parse_template_expression(template)

        self.assertIsNotNone(ast)
        self.assertEqual(2, len(ast.children))
        self.assertIsInstance(ast.children[0], TemplateWordNode)
        self.assertIsInstance(ast.children[1], TemplateWordNode)


if __name__ == '__main__':
    unittest.main()

import unittest
import xml.etree.ElementTree as ET

from test.parser.template.graph.test_graph_client import TemplateGraphTestClient


class TemplateGraphThatTests(TemplateGraphTestClient):

    def test_that_index_as_attrib_full(self):
        template = ET.fromstring("""
            <template>
                <that index="1"></that>
            </template>
            """)
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertEqual(ast.children[0].to_string(), "THAT Index=1")

    def test_thatstar_index_as_attrib_full(self):
        template = ET.fromstring("""
			<template>
				<thatstar index="1"></thatstar>
			</template>
			""")
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertEqual(ast.children[0].to_string(), "THATSTAR Index=1")
        self.assertEqual(ast.resolve(self.test_bot, self.test_clientid), "*")


if __name__ == '__main__':
    unittest.main()

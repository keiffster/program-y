import unittest
import xml.etree.ElementTree as ET

from test.parser.template.graph.test_graph_client import TemplateGraphTestClient


class TemplateGraphSystemTests(TemplateGraphTestClient):

    def test_system_timeout_as_attrib_full(self):
        template = ET.fromstring("""
			<template>
				<system timeout="1000">echo "Hello World"</system>
			</template>
			""")
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertEqual(ast.resolve(self.test_bot, self.test_clientid), "Hello World")

    def test_size(self):
        template = ET.fromstring("""
			<template>
				<size />
			</template>
			""")
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertEqual(ast.resolve(self.test_bot, self.test_clientid), "0")


if __name__ == '__main__':
    unittest.main()

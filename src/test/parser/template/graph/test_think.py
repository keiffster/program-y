import unittest
import xml.etree.ElementTree as ET

from test.parser.template.graph.test_graph_client import TemplateGraphTestClient


class TemplateGraphThinkTests(TemplateGraphTestClient):

    def test_think(self):
        template = ET.fromstring("""
			<template>
				<think>XYZ</think>
			</template>
			""")
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertEqual(ast.resolve(None, None), "")


if __name__ == '__main__':
    unittest.main()

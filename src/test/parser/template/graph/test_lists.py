import unittest
import xml.etree.ElementTree as ET

from test.parser.template.graph.test_graph_client import TemplateGraphTestClient


class TemplateGraphListProcessingTests(TemplateGraphTestClient):

    def test_first(self):
        template = ET.fromstring("""
            <template>
                <first>one two three four</first>
            </template>
            """)
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertEqual(ast.resolve(None, None), "one")

    def test_rest(self):
        template = ET.fromstring("""
            <template>
                <rest>one two three four</rest>
            </template>
            """)
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertEqual(ast.resolve(None, None), "two three four")

if __name__ == '__main__':
    unittest.main()

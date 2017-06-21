import unittest
import xml.etree.ElementTree as ET

from test.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphRestTests(TemplateGraphTestClient):

    def test_rest(self):
        template = ET.fromstring("""
            <template>
                <rest>one two three four</rest>
            </template>
            """)
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertEqual(ast.resolve(None, None), "two three four")


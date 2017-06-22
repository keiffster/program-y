import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.date import TemplateDateNode

from test.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphDateTests(TemplateGraphTestClient):

    def test_date_format_as_attrib(self):
        template = ET.fromstring("""
            <template>
                <date format="%c" />
            </template>
            """)
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        set_node = ast.children[0]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateDateNode)
        self.assertIsNotNone(ast.resolve(self.test_bot, self.test_clientid))

    def test_date_format_as_attrib_full(self):
        template = ET.fromstring("""
            <template>
                <date format="%c"></date>
            </template>
            """)
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        set_node = ast.children[0]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateDateNode)
        self.assertIsNotNone(ast.resolve(self.test_bot, self.test_clientid))

    def test_date_format_as_attrib_default(self):
        template = ET.fromstring("""
            <template>
                <date/>
            </template>
            """)
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        set_node = ast.children[0]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateDateNode)
        self.assertIsNotNone(ast.resolve(self.test_bot, self.test_clientid))


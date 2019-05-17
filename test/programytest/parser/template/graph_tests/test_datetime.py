import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.date import TemplateDateNode

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphDateTests(TemplateGraphTestClient):

    DEFAULT_DATETIME_REGEX = "^.{3}\s*.{3}\s*\d{1,}\s\d{2}:\d{2}:\d{2}\s\d{4}"

    def test_date_format_as_attrib(self):
        template = ET.fromstring("""
            <template>
                <date format="%c" />
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        date_node = ast.children[0]
        self.assertIsNotNone(date_node)
        self.assertIsInstance(date_node, TemplateDateNode)
        self.assertIsNotNone(ast.resolve(self._client_context))

        result = ast.resolve_to_string(self.create_client_context("testid"))
        self.assertIsNotNone(result)
        self.assertRegex(result, TemplateGraphDateTests.DEFAULT_DATETIME_REGEX)

    def test_date_format_as_attrib_full(self):
        template = ET.fromstring("""
            <template>
                <date format="%c"></date>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        date_node = ast.children[0]
        self.assertIsNotNone(date_node)
        self.assertIsInstance(date_node, TemplateDateNode)
        self.assertIsNotNone(ast.resolve(self._client_context))

        result = ast.resolve_to_string(self.create_client_context("testid"))
        self.assertIsNotNone(result)
        self.assertRegex(result,TemplateGraphDateTests.DEFAULT_DATETIME_REGEX)

    def test_date_format_as_child(self):
        template = ET.fromstring("""
            <template>
                <date><format>%c</format></date>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        date_node = ast.children[0]
        self.assertIsNotNone(date_node)
        self.assertIsInstance(date_node, TemplateDateNode)
        self.assertIsNotNone(ast.resolve(self._client_context))

        result = ast.resolve_to_string(self.create_client_context("testid"))
        self.assertIsNotNone(result)
        self.assertRegex(result, TemplateGraphDateTests.DEFAULT_DATETIME_REGEX)

    def test_date_format_as_attrib_default(self):
        template = ET.fromstring("""
            <template>
                <date/>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        date_node = ast.children[0]
        self.assertIsNotNone(date_node)
        self.assertIsInstance(date_node, TemplateDateNode)
        self.assertIsNotNone(ast.resolve(self._client_context))

        result = ast.resolve_to_string(self.create_client_context("testid"))
        self.assertIsNotNone(result)
        self.assertRegex(result, TemplateGraphDateTests.DEFAULT_DATETIME_REGEX)

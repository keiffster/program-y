import xml.etree.ElementTree as ET

from programy.parser.exceptions import ParserException
from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.interval import TemplateIntervalNode
from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphIntervalTests(TemplateGraphTestClient):

    def test_denormize_node_from_xml(self):
        template = ET.fromstring("""
            <template>
                <interval>
                    <format>%c</format>
                    <style>days</style>
                    <from>Wed Oct  5 16:35:11 2016</from>
                    <to>Fri Oct  7 16:35:11 2016</to>
                </interval>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        set_node = ast.children[0]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateIntervalNode)
        self.assertEqual(ast.resolve(self._client_context), "2")

    def test_interval_values_as_attribs(self):
        template = ET.fromstring("""
            <template>
                <interval format="%c" style="days" from="Wed Oct  5 16:35:11 2016" to="Fri Oct  7 16:35:11 2016" >
                </interval>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        set_node = ast.children[0]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateIntervalNode)
        self.assertEqual(ast.resolve(self._client_context), "2")

    def test_interval_style_with_child(self):
        template = ET.fromstring("""
            <template>
                <interval>
                    <format>%c</format>
                    <style><lowercase>DAYS</lowercase></style>
                    <from>Wed Oct  5 16:35:11 2016</from>
                    <to>Fri Oct  7 16:35:11 2016</to>
                </interval>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        set_node = ast.children[0]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateIntervalNode)
        self.assertEqual(ast.resolve(self._client_context), "2")

    def test_interval_with_child(self):
        template = ET.fromstring("""
            <template>
                <interval>
                    <format>%c</format>
                    <style>days</style>
                    <from>Wed Oct  5 16:35:11 2016</from>
                    <to>Fri Oct  7 16:35:11 2016</to>
                    <lowercase>DAYS</lowercase>
                </interval>
            </template>
            """)

        with self.assertRaises(ParserException):
            _ = self._graph.parse_template_expression(template)

    def test_interval_resolve_no_format(self):
        template = ET.fromstring("""
            <template>
                <interval>
                    <style>days</style>
                    <from>Wed Oct  5 16:35:11 2016</from>
                    <to>Fri Oct  7 16:35:11 2016</to>
                </interval>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        set_node = ast.children[0]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateIntervalNode)
        self.assertEqual(ast.resolve(self._client_context), "2")

    def test_interval_resolve_no_style(self):
        template = ET.fromstring("""
            <template>
                <interval>
                    <format>%c</format>
                    <from>Wed Oct  5 16:35:11 2016</from>
                    <to>Fri Oct  7 16:35:11 2016</to>
                </interval>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        set_node = ast.children[0]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateIntervalNode)
        self.assertEqual(ast.resolve(self._client_context), "2")

    def test_interval_resolve_no_from(self):
        template = ET.fromstring("""
            <template>
                <interval>
                    <style>days</style>
                    <to>Fri Oct  7 16:35:11 2016</to>
                </interval>
            </template>
            """)

        with self.assertRaises(ParserException):
            ast = self._graph.parse_template_expression(template)

    def test_interval_resolve_no_to(self):
        template = ET.fromstring("""
            <template>
                <interval>
                    <style>days</style>
                    <from>Wed Oct  5 16:35:11 2016</from>
                </interval>
            </template>
            """)

        with self.assertRaises(ParserException):
            ast = self._graph.parse_template_expression(template)

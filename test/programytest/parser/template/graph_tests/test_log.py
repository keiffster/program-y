import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.log import TemplateLogNode

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphLogTests(TemplateGraphTestClient):

    def test_log_node_from_xml_default_values(self):
        template = ET.fromstring("""
            <template>
                <log>Text</log>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        log_node = ast.children[0]
        self.assertIsNotNone(log_node)
        self.assertIsInstance(log_node, TemplateLogNode)

        result = log_node.resolve(self.create_client_context("testid"))
        self.assertIsNotNone(result)

    def test_log_node_from_xml_logging(self):
        template = ET.fromstring("""
            <template>
                <log output="logging">Text</log>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        log_node = ast.children[0]
        self.assertIsNotNone(log_node)
        self.assertIsInstance(log_node, TemplateLogNode)

        result = log_node.resolve(self.create_client_context("testid"))
        self.assertIsNotNone(result)

    def test_log_node_from_xml_logging_as_child(self):
        template = ET.fromstring("""
            <template>
                <log>
                    <output>logging</output>
                    Text
                </log>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        log_node = ast.children[0]
        self.assertIsNotNone(log_node)
        self.assertIsInstance(log_node, TemplateLogNode)

        result = log_node.resolve(self.create_client_context("testid"))
        self.assertIsNotNone(result)

    def test_log_node_from_xml_logging_level(self):
        template = ET.fromstring("""
            <template>
                <log output="logging" level="debug">Text</log>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        log_node = ast.children[0]
        self.assertIsNotNone(log_node)
        self.assertIsInstance(log_node, TemplateLogNode)

        result = log_node.resolve(self.create_client_context("testid"))
        self.assertIsNotNone(result)

    def test_log_node_from_xml_logging_level_as_children(self):
        template = ET.fromstring("""
            <template>
                <log>
                    <output>logging</output>
                    <level>debug</level>
                    Text
                </log>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        log_node = ast.children[0]
        self.assertIsNotNone(log_node)
        self.assertIsInstance(log_node, TemplateLogNode)

        result = log_node.resolve(self.create_client_context("testid"))
        self.assertIsNotNone(result)

    def test_log_node_from_xml_print(self):
        template = ET.fromstring("""
            <template>
                <log output="print">Text</log>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        log_node = ast.children[0]
        self.assertIsNotNone(log_node)
        self.assertIsInstance(log_node, TemplateLogNode)

        result = log_node.resolve(self.create_client_context("testid"))
        self.assertIsNotNone(result)

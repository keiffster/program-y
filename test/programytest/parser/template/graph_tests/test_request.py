import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.template.nodes.get import TemplateGetNode
from programy.parser.template.nodes.request import TemplateRequestNode
from programy.parser.exceptions import ParserException

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphRequestTests(TemplateGraphTestClient):

    def test_request_index_as_attrib_full(self):
        template = ET.fromstring("""
            <template>
                <request index="8"></request>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        req_node = ast.children[0]
        self.assertIsNotNone(req_node)
        self.assertIsInstance(req_node, TemplateRequestNode)

        self.assertIsNotNone(req_node.index)
        self.assertIsInstance(req_node.index, TemplateWordNode)

    def test_request_index_as_child(self):
        template = ET.fromstring("""
            <template>
                <request><index>8</index></request>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        req_node = ast.children[0]
        self.assertIsNotNone(req_node)
        self.assertIsInstance(req_node, TemplateRequestNode)

        self.assertIsNotNone(req_node.index)
        self.assertIsInstance(req_node.index, TemplateNode)

    def test_request_index_as_children(self):
        template = ET.fromstring("""
            <template>
                <request><index><get name="count" /></index></request>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        req_node = ast.children[0]
        self.assertIsNotNone(req_node)
        self.assertIsInstance(req_node, TemplateRequestNode)

        self.assertIsNotNone(req_node.index)
        self.assertIsInstance(req_node.index, TemplateNode)

        self.assertEquals(1, len(req_node.index.children))
        self.assertIsInstance(req_node.index.children[0], TemplateGetNode)

    def test_request_with_children(self):
        template = ET.fromstring("""
            <template>
                <request index="8">Something</request>
            </template>
            """)
        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template)

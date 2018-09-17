import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.first import TemplateFirstNode
from programy.parser.template.nodes.word import TemplateWordNode
from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphFirstTests(TemplateGraphTestClient):

    def test_first(self):
        template = ET.fromstring("""
            <template>
                <first>one two three four</first>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertEqual(1, len(ast.children))

        first_node = ast.children[0]
        self.assertIsNotNone(first_node)
        self.assertIsInstance(first_node, TemplateFirstNode)

        self.assertIsNotNone(first_node.children)
        self.assertEqual(4, len(first_node.children))
        self.assertIsInstance(first_node.children[0], TemplateWordNode)

        self.assertEqual(ast.resolve(self._client_context), "one")

    def test_first_one_word(self):
        template = ET.fromstring("""
            <template>
                <first>one</first>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)

        self.assertEqual(ast.resolve(self._client_context), "one")

    def test_first_empty(self):
        template = ET.fromstring("""
            <template>
                <first></first>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)

        self.assertEqual(ast.resolve(self._client_context), "NIL")



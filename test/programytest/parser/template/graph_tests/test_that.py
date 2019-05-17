import unittest
import xml.etree.ElementTree as ET

from programy.parser.template.nodes.that import TemplateThatNode

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient
from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.that import TemplateThatNode


class TemplateGraphThatTests(TemplateGraphTestClient):

    def test_that_index_default(self):
        template = ET.fromstring("""
            <template>
                <that/>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        self.assertEqual(ast.children[0].to_string(), "[THAT[WORD]1]")

        date_node = ast.children[0]
        self.assertIsNotNone(date_node)
        self.assertIsInstance(date_node, TemplateThatNode)
        self.assertIsNotNone(ast.resolve(self._client_context))

        result = ast.resolve_to_string(self.create_client_context("testid"))
        self.assertIsNotNone(result)

    def test_that_index_as_attrib(self):
        template = ET.fromstring("""
            <template>
                <that index="1"></that>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        self.assertEqual(ast.children[0].to_string(), "[THAT[WORD]1]")

        date_node = ast.children[0]
        self.assertIsNotNone(date_node)
        self.assertIsInstance(date_node, TemplateThatNode)
        self.assertIsNotNone(ast.resolve(self._client_context))

        result = ast.resolve_to_string(self.create_client_context("testid"))
        self.assertIsNotNone(result)

    def test_that_question_sentnce_as_attrib(self):
        template = ET.fromstring("""
            <template>
                <that index="1, 1"></that>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        self.assertEqual(ast.children[0].to_string(), "[THAT[WORD]1, 1]")

        date_node = ast.children[0]
        self.assertIsNotNone(date_node)
        self.assertIsInstance(date_node, TemplateThatNode)
        self.assertIsNotNone(ast.resolve(self._client_context))

        result = ast.resolve_to_string(self.create_client_context("testid"))
        self.assertIsNotNone(result)

    def test_that_index_as_child(self):
        template = ET.fromstring("""
            <template>
                <that>
                    <index>1</index>
                </that>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        self.assertEqual(ast.children[0].to_string(), "[THAT[NODE]]")

        date_node = ast.children[0]
        self.assertIsNotNone(date_node)
        self.assertIsInstance(date_node, TemplateThatNode)
        self.assertIsNotNone(ast.resolve(self._client_context))

        result = ast.resolve_to_string(self.create_client_context("testid"))
        self.assertIsNotNone(result)

    def test_that_question_sentence_as_child(self):
        template = ET.fromstring("""
            <template>
                <that>
                    <index>1, 1</index>
                </that>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        self.assertEqual(ast.children[0].to_string(), "[THAT[NODE]]")

        date_node = ast.children[0]
        self.assertIsNotNone(date_node)
        self.assertIsInstance(date_node, TemplateThatNode)
        self.assertIsNotNone(ast.resolve(self._client_context))

        result = ast.resolve_to_string(self.create_client_context("testid"))
        self.assertIsNotNone(result)

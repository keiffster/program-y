import unittest
import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.template.nodes.star import TemplateStarNode

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphStarTests(TemplateGraphTestClient):

    def test_star_no_index_full(self):
        template = ET.fromstring("""
            <template>
                <star></star>
            </template>
        """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsNotNone(ast.children)
        self.assertEqual(1, len(ast.children))
        self.assertIsInstance(ast.children[0], TemplateStarNode)
        self.assertEqual(ast.resolve(self._client_context), "one")

    def test_star_no_index_full_embedded(self):
        template = ET.fromstring("""
            <template>
                Hello <star></star>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsNotNone(ast.children)
        self.assertEqual(2, len(ast.children))
        self.assertIsInstance(ast.children[0], TemplateWordNode)
        self.assertIsInstance(ast.children[1], TemplateStarNode)
        self.assertEqual(ast.resolve(self._client_context), "Hello one")

    def test_star_no_index_short(self):
        template = ET.fromstring("""
			<template>
				<star />
			</template>
			""")
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsNotNone(ast.children)
        self.assertEqual(1, len(ast.children))
        self.assertIsInstance(ast.children[0], TemplateStarNode)
        self.assertEqual(ast.resolve(self._client_context), "one")

    def test_star_index_as_child(self):
        template = ET.fromstring("""
			<template>
				<star><index>2</index></star>
			</template>
			""")
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsNotNone(ast.children)
        self.assertEqual(1, len(ast.children))
        self.assertIsInstance(ast.children[0], TemplateStarNode)
        self.assertEqual(ast.resolve(self._client_context), "two")

    def test_star_index_as_attrib_full(self):
        template = ET.fromstring("""
			<template>
				<star index="3"></star>
			</template>
			""")
        ast = self._graph.parse_template_expression(template)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast)
        self.assertIsNotNone(ast.children)
        self.assertEqual(1, len(ast.children))
        self.assertIsInstance(ast.children[0], TemplateStarNode)
        self.assertEqual(ast.resolve(self._client_context), "three")

    def test_star_index_as_attrib_short(self):
        template = ET.fromstring("""
			<template>
				<star index="4" />
			</template>
			""")
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsNotNone(ast.children)
        self.assertEqual(1, len(ast.children))
        self.assertIsInstance(ast.children[0], TemplateStarNode)
        self.assertEqual(ast.resolve(self._client_context), "four")


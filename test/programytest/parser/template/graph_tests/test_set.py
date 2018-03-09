import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.set import TemplateSetNode
from programy.parser.exceptions import ParserException

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphSetTests(TemplateGraphTestClient):

    def test_set_template_predicate_as_attrib(self):
        template = ET.fromstring("""
			<template>
				<set name="somepred">Value1</set>
			</template>
			""")
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        set_node = ast.children[0]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateSetNode)
        self.assertIsNotNone(set_node.name)
        self.assertIsInstance(set_node.name, TemplateNode)
        self.assertEqual(set_node.name.resolve(self._client_context), "somepred")
        self.assertFalse(set_node.local)

        self.assertEqual(len(set_node.children), 1)
        self.assertEqual(set_node.children[0].resolve(self._client_context), "Value1")

    def test_set_template_multi_word_predicate_as_attrib(self):
        template = ET.fromstring("""
            <template>
                <set name="somepred other">Value1</set>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        set_node = ast.children[0]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateSetNode)
        self.assertIsNotNone(set_node.name)
        self.assertIsInstance(set_node.name, TemplateNode)
        self.assertEqual(set_node.name.resolve(self._client_context), "somepred other")
        self.assertFalse(set_node.local)

        self.assertEqual(len(set_node.children), 1)
        self.assertEqual(set_node.children[0].resolve(self._client_context), "Value1")

    def test_set_template_predicate_nested(self):
        template = ET.fromstring("""
			<template>
				Some text here
				<set name="somepred">Value1</set>
				Some text there
			</template>
			""")
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 7)

        set_node = ast.children[3]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateSetNode)
        self.assertIsNotNone(set_node.name)
        self.assertIsInstance(set_node.name, TemplateNode)
        self.assertEqual(set_node.name.resolve(self._client_context), "somepred")
        self.assertFalse(set_node.local)

        self.assertEqual(len(set_node.children), 1)
        self.assertEqual(set_node.children[0].resolve(self._client_context), "Value1")

    def test_set_template_local_as_attrib(self):
        template = ET.fromstring("""
			<template>
				<set var="somevar">Value2</set>
			</template>
			""")
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        set_node = ast.children[0]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateSetNode)
        self.assertIsNotNone(set_node.name)
        self.assertIsInstance(set_node.name, TemplateNode)
        self.assertEqual(set_node.name.resolve(self._client_context), "somevar")
        self.assertTrue(set_node.local)

        self.assertEqual(len(set_node.children), 1)
        self.assertEqual(set_node.children[0].resolve(self._client_context), "Value2")

    def test_set_template_predicate_as_child(self):
        template = ET.fromstring("""
			<template>
				<set><name>somepred</name>Value3</set>
			</template>
			""")
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        set_node = ast.children[0]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateSetNode)
        self.assertIsNotNone(set_node.name)
        self.assertIsInstance(set_node.name, TemplateNode)
        self.assertEqual(set_node.name.resolve(self._client_context), "somepred")
        self.assertFalse(set_node.local)

        self.assertEqual(len(set_node.children), 1)
        self.assertEqual(set_node.children[0].resolve(self._client_context), "Value3")

    def test_set_template_local_as_child(self):
        template = ET.fromstring("""
			<template>
				<set><var>somepred</var>Value4</set>
			</template>
			""")
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        set_node = ast.children[0]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateSetNode)
        self.assertIsNotNone(set_node.name)
        self.assertIsInstance(set_node.name, TemplateNode)
        self.assertEqual(set_node.name.resolve(self._client_context), "somepred")
        self.assertTrue(set_node.local)

        self.assertEqual(len(set_node.children), 1)
        self.assertEqual(set_node.children[0].resolve(self._client_context), "Value4")

    def test_set_name_and_var(self):
        template = ET.fromstring("""
                <template>
                    <set name="somepred" var="somevar">Value1</set>
                </template>
                """)
        with self.assertRaises(ParserException):
            ast = self._graph.parse_template_expression(template)

    def test_set_no_name_or_var(self):
        template = ET.fromstring("""
                <template>
                    <set>Value1</set>
                </template>
                """)
        with self.assertRaises(ParserException):
            ast = self._graph.parse_template_expression(template)

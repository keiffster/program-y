import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.get import TemplateGetNode
from programy.parser.exceptions import ParserException

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphGetTests(TemplateGraphTestClient):

    def test_get_template_predicate_as_attrib(self):
        template = ET.fromstring("""
			<template>
				<get name="somepred" />
			</template>
			""")
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        get_node = ast.children[0]
        self.assertIsNotNone(get_node)
        self.assertIsInstance(get_node, TemplateGetNode)
        self.assertIsNotNone(get_node.name)
        self.assertIsInstance(get_node.name, TemplateNode)
        self.assertEqual(get_node.name.resolve(self._client_context), "somepred")
        self.assertFalse(get_node.local)

    def test_get_template_predicate_as_attrib_mixed(self):
        template = ET.fromstring("""
			<template>
				Hello <get name="somepred" /> how are you
			</template>
			""")
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 5)

        get_node = ast.children[1]
        self.assertIsNotNone(get_node)
        self.assertIsInstance(get_node, TemplateGetNode)
        self.assertIsNotNone(get_node.name)
        self.assertIsInstance(get_node.name, TemplateNode)
        self.assertEqual(get_node.name.resolve(self._client_context), "somepred")
        self.assertFalse(get_node.local)

    def test_get_template_var_as_attrib(self):
        template = ET.fromstring("""
			<template>
				<get var="somevar" />
			</template>
			""")
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        get_node = ast.children[0]
        self.assertIsNotNone(get_node)
        self.assertIsInstance(get_node, TemplateGetNode)
        self.assertIsNotNone(get_node.name)
        self.assertIsInstance(get_node.name, TemplateNode)
        self.assertEqual(get_node.name.resolve(self._client_context), "somevar")
        self.assertTrue(get_node.local)

    def test_get_template_predicate_as_child(self):
        template = ET.fromstring("""
			<template>
				<get><name>somepred as text</name></get>
			</template>
			""")
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        get_node = ast.children[0]
        self.assertIsNotNone(get_node)
        self.assertIsInstance(get_node, TemplateGetNode)
        self.assertIsNotNone(get_node.name)
        self.assertIsInstance(get_node.name, TemplateNode)
        self.assertEqual(get_node.name.resolve(self._client_context), "somepred as text")
        self.assertFalse(get_node.local)

    def test_get_template_local_as_child(self):
        template = ET.fromstring("""
			<template>
				<get><var>somevar</var></get>
			</template>
			""")
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        get_node = ast.children[0]
        self.assertIsNotNone(get_node)
        self.assertIsInstance(get_node, TemplateGetNode)
        self.assertIsNotNone(get_node.name)
        self.assertIsInstance(get_node.name, TemplateNode)
        self.assertEqual(get_node.name.resolve(self._client_context), "somevar")
        self.assertTrue(get_node.local)

    def test_get_template_name_and_var(self):
        template = ET.fromstring("""
			<template>
				<get name="somename" var="somevar" />
			</template>
			""")
        with self.assertRaises(ParserException):
            ast = self._graph.parse_template_expression(template)

    def test_get_template_other_than_name_and_var(self):
        template = ET.fromstring("""
			<template>
				<get><id>somevar</id></get>
			</template>
			""")
        with self.assertRaises(ParserException):
            ast = self._graph.parse_template_expression(template)

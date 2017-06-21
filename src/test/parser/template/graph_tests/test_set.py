import unittest
import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.set import TemplateSetNode

from test.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphSetTests(TemplateGraphTestClient):

    def test_set_template_predicate_as_attrib(self):
        template = ET.fromstring("""
			<template>
				<set name="somepred">Value1</set>
			</template>
			""")
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        set_node = ast.children[0]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateSetNode)
        self.assertIsNotNone(set_node.name)
        self.assertIsInstance(set_node.name, TemplateNode)
        self.assertEqual(set_node.name.resolve(None, None), "somepred")
        self.assertFalse(set_node.local)

        self.assertEqual(len(set_node.children), 1)
        self.assertEqual(set_node.children[0].resolve(None, None), "Value1")

    def test_set_template_multi_word_predicate_as_attrib(self):
        template = ET.fromstring("""
            <template>
                <set name="somepred other">Value1</set>
            </template>
            """)
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        set_node = ast.children[0]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateSetNode)
        self.assertIsNotNone(set_node.name)
        self.assertIsInstance(set_node.name, TemplateNode)
        self.assertEqual(set_node.name.resolve(None, None), "somepred other")
        self.assertFalse(set_node.local)

        self.assertEqual(len(set_node.children), 1)
        self.assertEqual(set_node.children[0].resolve(None, None), "Value1")

    def test_set_template_predicate_nested(self):
        template = ET.fromstring("""
			<template>
				Some text here
				<set name="somepred">Value1</set>
				Some text there
			</template>
			""")
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 7)

        set_node = ast.children[3]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateSetNode)
        self.assertIsNotNone(set_node.name)
        self.assertIsInstance(set_node.name, TemplateNode)
        self.assertEqual(set_node.name.resolve(None, None), "somepred")
        self.assertFalse(set_node.local)

        self.assertEqual(len(set_node.children), 1)
        self.assertEqual(set_node.children[0].resolve(None, None), "Value1")

    def test_set_template_local_as_attrib(self):
        template = ET.fromstring("""
			<template>
				<set var="somevar">Value2</set>
			</template>
			""")
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        set_node = ast.children[0]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateSetNode)
        self.assertIsNotNone(set_node.name)
        self.assertIsInstance(set_node.name, TemplateNode)
        self.assertEqual(set_node.name.resolve(None, None), "somevar")
        self.assertTrue(set_node.local)

        self.assertEqual(len(set_node.children), 1)
        self.assertEqual(set_node.children[0].resolve(None, None), "Value2")

    def test_set_template_predicate_as_child(self):
        template = ET.fromstring("""
			<template>
				<set><name>somepred</name>Value3</set>
			</template>
			""")
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        set_node = ast.children[0]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateSetNode)
        self.assertIsNotNone(set_node.name)
        self.assertIsInstance(set_node.name, TemplateNode)
        self.assertEqual(set_node.name.resolve(None, None), "somepred")
        self.assertFalse(set_node.local)

        self.assertEqual(len(set_node.children), 1)
        self.assertEqual(set_node.children[0].resolve(None, None), "Value3")

    def test_set_template_local_as_child(self):
        template = ET.fromstring("""
			<template>
				<set><var>somepred</var>Value4</set>
			</template>
			""")
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        set_node = ast.children[0]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateSetNode)
        self.assertIsNotNone(set_node.name)
        self.assertIsInstance(set_node.name, TemplateNode)
        self.assertEqual(set_node.name.resolve(None, None), "somepred")
        self.assertTrue(set_node.local)

        self.assertEqual(len(set_node.children), 1)
        self.assertEqual(set_node.children[0].resolve(None, None), "Value4")


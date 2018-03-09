import xml.etree.ElementTree as ET
import unittest

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.extension import TemplateExtensionNode

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TestExtension(object):

    def execute(self, context, data):
        return "executed"


class TemplateGraphBotTests(TemplateGraphTestClient):

    def test_extension_as_attrib(self):
        template = ET.fromstring("""
			<template>
				<extension path="programytest.parser.template.graph_tests.test_extension.TestExtension">
				1 2 3
				</extension>
			</template>
			""")
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        ext_node = ast.children[0]
        self.assertIsNotNone(ext_node)
        self.assertIsInstance(ext_node, TemplateExtensionNode)
        self.assertIsNotNone(ext_node._path)

        self.assertEqual(len(ext_node.children), 3)
        self.assertEqual("executed", ext_node.resolve(self._client_context))

    def test_extension_as_child(self):
        template = ET.fromstring("""
            <template>
                <extension>
                    <path>programytest.parser.template.graph_tests.test_extension.TestExtension</path>
                    1 2 3
                </extension>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        ext_node = ast.children[0]
        self.assertIsNotNone(ext_node)
        self.assertIsInstance(ext_node, TemplateExtensionNode)
        self.assertIsNotNone(ext_node._path)

        self.assertEqual(len(ext_node.children), 3)
        self.assertEqual("executed", ext_node.resolve(self._client_context))


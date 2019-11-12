import xml.etree.ElementTree as ET

from programy.config.brain.brain import BrainConfiguration
from programy.parser.exceptions import ParserException
from programy.parser.template.nodes.authorise import TemplateAuthoriseNode
from programy.parser.template.nodes.base import TemplateNode
from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphAuthoriseTests(TemplateGraphTestClient):

    def get_brain_config(self):
        return BrainConfiguration()

    def test_authorise_with_role_as_attrib(self):
        template = ET.fromstring("""
			<template>
				<authorise role="root">
				Hello
				</authorise>
			</template>
			""")

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        auth_node = ast.children[0]
        self.assertIsNotNone(auth_node)
        self.assertIsInstance(auth_node, TemplateAuthoriseNode)
        self.assertIsNotNone(auth_node.role)
        self.assertEqual("root", auth_node.role)

        result = auth_node.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("Hello", result)

    def test_authorise_with_role_as_attrib_and_optional_srai(self):
        template = ET.fromstring("""
			<template>
				<authorise role="root" denied_srai="ACCESS_DENIED">
				Hello
				</authorise>
			</template>
			""")

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        auth_node = ast.children[0]
        self.assertIsNotNone(auth_node)
        self.assertIsInstance(auth_node, TemplateAuthoriseNode)
        self.assertIsNotNone(auth_node.role)
        self.assertEqual("root", auth_node.role)

        result = auth_node.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("Hello", result)

    def test_authorise_with_role_missing_as_attrib(self):
        template = ET.fromstring("""
            <template>
                <authorise denied_srai="ACCESS_DENIED">
                Hello
                </authorise>
            </template>
            """)

        with self.assertRaises(ParserException):
            _ = self._graph.parse_template_expression(template)

    def test_authorise_with_denie_srai_empty_as_attrib(self):
        template = ET.fromstring("""
            <template>
				<authorise role="root" denied_srai="">
                Hello
                </authorise>
            </template>
            """)

        with self.assertRaises(ParserException):
            _ = self._graph.parse_template_expression(template)

    def test_authorise_with_role_with_children(self):
        template = ET.fromstring("""
            <template>
                <authorise role="root" denied_srai="ACCESS_DENIED">
                <id />
                </authorise>
            </template>
            """)

        ast = self._graph.parse_template_expression(template)
        self.assertEquals(1, len(ast.children))

    def test_authorise_with_role_missing(self):
        template = ET.fromstring("""
                <template>
                    <authorise denied_srai="ACCESS_DENIED">
                    Hello
                    </authorise>
                </template>
                """)

        with self.assertRaises(ParserException):
            _ = self._graph.parse_template_expression(template)

    def test_authorise_with_role_empty(self):
        template = ET.fromstring("""
                <template>
                    <authorise role="" denied_srai="ACCESS_DENIED">
                    Hello
                    </authorise>
                </template>
                """)

        with self.assertRaises(ParserException):
            _ = self._graph.parse_template_expression(template)

    def test_authorise_with_denied_srai_empty(self):
        template = ET.fromstring("""
                <template>
                    <authorise role="" denied_srai="">
                    Hello
                    </authorise>
                </template>
                """)

        with self.assertRaises(ParserException):
            _ = self._graph.parse_template_expression(template)

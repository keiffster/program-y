import xml.etree.ElementTree as ET

from programy.parser.exceptions import ParserException
from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.richmedia.button import TemplateButtonNode
from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphButtonTests(TemplateGraphTestClient):

    def test_url_button_node_from_xml(self):
        template = ET.fromstring("""
			<template>
				<button>
				    <text>Servusai.com</text>
				    <url>http://www.servusai.com</url>
				</button>
			</template>
			""")
        root = self._graph.parse_template_expression(template)
        self.assertIsNotNone(root)
        self.assertIsInstance(root, TemplateNode)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 1)

        node = root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, TemplateButtonNode)

        self.assertIsNotNone(node._text)
        self.assertIsNotNone(node._url)
        self.assertIsNone(node._postback)

    def test_url_button_with_attribs_url(self):
        template = ET.fromstring("""
            <template>
                <button text="Servusai.com" url="http://www.servusai.com" >
                </button>
            </template>
            """)
        root = self._graph.parse_template_expression(template)
        self.assertIsNotNone(root)
        self.assertIsInstance(root, TemplateNode)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 1)

        node = root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, TemplateButtonNode)

        self.assertIsNotNone(node._text)
        self.assertIsNotNone(node._url)

    def test_url_button_with_attribs_postback(self):
        template = ET.fromstring("""
            <template>
                <button text="Servusai.com" postback="HELLO WORLD" >
                </button>
            </template>
            """)
        root = self._graph.parse_template_expression(template)
        self.assertIsNotNone(root)
        self.assertIsInstance(root, TemplateNode)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 1)

        node = root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, TemplateButtonNode)

        self.assertIsNotNone(node._text)
        self.assertIsNotNone(node._postback)

    def test_postback_button_node_from_xml(self):
        template = ET.fromstring("""
			<template>
				<button>
				    <text>Servusai.com</text>
				    <postback>SERVUSAI DOT COM</postback>
				</button>
			</template>
			""")
        root = self._graph.parse_template_expression(template)
        self.assertIsNotNone(root)
        self.assertIsInstance(root, TemplateNode)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 1)

        node = root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, TemplateButtonNode)

        self.assertIsNotNone(node._text)
        self.assertIsNone(node._url)
        self.assertIsNotNone(node._postback)

    def test_button_no_text(self):
        template = ET.fromstring("""
			<template>
				<button>
				    <postback>SERVUSAI DOT COM</postback>
				</button>
			</template>
			""")

        with self.assertRaises(ParserException):
            _ = self._graph.parse_template_expression(template)

    def test_button_no_url_or_postback(self):
        template = ET.fromstring("""
			<template>
				<button>
				    <text>Servusai.com</text>
				</button>
			</template>
			""")

        with self.assertRaises(ParserException):
            _ = self._graph.parse_template_expression(template)

    def test_button_invalid_children(self):
        template = ET.fromstring("""
			<template>
				<button>
				    <text>Servusai.com</text>
                    <postback>SERVUSAI DOT COM</postback>
                    <id />
				</button>
			</template>
			""")

        with self.assertRaises(ParserException):
            _ = self._graph.parse_template_expression(template)

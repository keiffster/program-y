import xml.etree.ElementTree as ET

from programy.parser.exceptions import ParserException
from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.richmedia.reply import TemplateReplyNode
from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphReplyTests(TemplateGraphTestClient):

    def test_text_reply_node_from_xml(self):
        template = ET.fromstring("""
			<template>
				<reply>
				    <text>Servusai.com</text>
				</reply>
			</template>
			""")
        root = self._graph.parse_template_expression(template)
        self.assertIsNotNone(root)
        self.assertIsInstance(root, TemplateNode)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 1)

        node = root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, TemplateReplyNode)

        self.assertIsNotNone(node._text)
        self.assertIsNone(node._postback)

    def test_text_postback_reply_node_from_xml(self):
        template = ET.fromstring("""
			<template>
				<reply>
				    <text>Servusai.com</text>
				    <postback>SERVUSAI DOT COM</postback>
				</reply>
			</template>
			""")
        root = self._graph.parse_template_expression(template)
        self.assertIsNotNone(root)
        self.assertIsInstance(root, TemplateNode)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 1)

        node = root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, TemplateReplyNode)

        self.assertIsNotNone(node._text)
        self.assertIsNotNone(node._postback)

    def test_text_as_attribs(self):
        template = ET.fromstring("""
            <template>
                <reply text="Servusai.com" postback="SERVUSAI DOT COM">
                </reply>
            </template>
            """)
        root = self._graph.parse_template_expression(template)
        self.assertIsNotNone(root)
        self.assertIsInstance(root, TemplateNode)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 1)

        node = root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, TemplateReplyNode)

        self.assertIsNotNone(node._text)
        self.assertIsNotNone(node._postback)

    def test_text_postback_as_attribs(self):
        template = ET.fromstring("""
            <template>
                <reply text="Servusai.com" postback="SERVUSAI DOT COM" />
            </template>
            """)
        root = self._graph.parse_template_expression(template)
        self.assertIsNotNone(root)
        self.assertIsInstance(root, TemplateNode)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 1)

        node = root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, TemplateReplyNode)

        self.assertIsNotNone(node._text)
        self.assertIsNotNone(node._postback)

    def test_reply_no_text(self):
        template = ET.fromstring("""
                <template>
                    <reply>
                        <postback>SERVUSAI DOT COM</postback>
                    </reply>
                </template>
                """)

        with self.assertRaises(ParserException):
            _ = self._graph.parse_template_expression(template)

    def test_reply_invalid_childrenl(self):
        template = ET.fromstring("""
                <template>
                    <reply>
                        <id />
                    </reply>
                </template>
                """)

        with self.assertRaises(ParserException):
            _ = self._graph.parse_template_expression(template)

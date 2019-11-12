import xml.etree.ElementTree as ET

from programy.parser.exceptions import ParserException
from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.richmedia.card import TemplateCardNode
from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphCardTests(TemplateGraphTestClient):

    def test_card_node_from_xml(self):
        template = ET.fromstring("""
			<template>
				<card>
				    <image>http://www.servusai.com/aiml.png</image>
				    <title>Servusai.com</title>
				    <subtitle>The home of ProgramY</subtitle>
                    <button>
                        <text>Servusai.com</text>
                        <url>http://www.servusai.com</url>
                    </button>
                    <button>
                        <text>ProgramY</text>
                        <url>http://github.io/keiffster</url>
                    </button>
				</card>
			</template>
			""")
        root = self._graph.parse_template_expression(template)
        self.assertIsNotNone(root)
        self.assertIsInstance(root, TemplateNode)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 1)

        node = root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, TemplateCardNode)

        self.assertIsNotNone(node._image)
        self.assertIsNotNone(node._title)
        self.assertIsNotNone(node._subtitle)
        self.assertIsNotNone(node._buttons)
        self.assertEqual(2, len(node._buttons))

    def test_card_attribs_as_xml(self):
        template = ET.fromstring("""
            <template>
                <card image="http://www.servusai.com/aiml.png" title="Servusai.com" subtitle="The home of ProgramY">
                    <button>
                        <text>Servusai.com</text>
                        <url>http://www.servusai.com</url>
                    </button>
                    <button>
                        <text>ProgramY</text>
                        <url>http://github.io/keiffster</url>
                    </button>
                </card>
            </template>
            """)
        root = self._graph.parse_template_expression(template)
        self.assertIsNotNone(root)
        self.assertIsInstance(root, TemplateNode)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 1)

        node = root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, TemplateCardNode)

        self.assertIsNotNone(node._image)
        self.assertIsNotNone(node._title)
        self.assertIsNotNone(node._subtitle)
        self.assertIsNotNone(node._buttons)
        self.assertEqual(2, len(node._buttons))

    def test_no_buttons(self):
        template = ET.fromstring("""
        			<template>
        				<card>
        				    <image>http://www.servusai.com/aiml.png</image>
        				    <title>Servusai.com</title>
        				    <subtitle>The home of ProgramY</subtitle>
        				</card>
        			</template>
        			""")

        with self.assertRaises(ParserException):
            _ = self._graph.parse_template_expression(template)

    def test_no_title(self):
        template = ET.fromstring("""
        			<template>
        				<card>
                            <button>
                                <text>ProgramY</text>
                                <url>http://github.io/keiffster</url>
                            </button>
        				</card>
        			</template>
        			""")

        with self.assertRaises(ParserException):
            _ = self._graph.parse_template_expression(template)

    def test_only_title_and_buttons(self):
        template = ET.fromstring("""
        			<template>
        				<card>
        				    <title>Servusai.com</title>
                            <button>
                                <text>ProgramY</text>
                                <url>http://github.io/keiffster</url>
                            </button>
        				</card>
        			</template>
        			""")

        _ = self._graph.parse_template_expression(template)

    def test_invalid_children(self):
        template = ET.fromstring("""
        			<template>
        				<card>
                            <button>
                                <text>ProgramY</text>
                                <url>http://github.io/keiffster</url>
                            </button>
                            <id />
        				</card>
        			</template>
        			""")

        with self.assertRaises(ParserException):
            _ = self._graph.parse_template_expression(template)


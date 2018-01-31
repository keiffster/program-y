import unittest

import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.template.nodes.srai import TemplateSRAINode

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphSraiTests(TemplateGraphTestClient):

    def test_srai_template_simple(self):
        template = ET.fromstring("""
            <template>
                <srai>
                    SRAI this text
                </srai>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateSRAINode)

        self.assertIsNotNone(ast.children[0].children)
        self.assertEqual(3, len(ast.children[0].children))
        self.assertIsInstance(ast.children[0].children[0], TemplateWordNode)
        self.assertIsInstance(ast.children[0].children[1], TemplateWordNode)
        self.assertIsInstance(ast.children[0].children[2], TemplateWordNode)

    def test_srai_template_nested(self):
        template = ET.fromstring("""
            <template>
                <srai>
                    SRAI This and <srai>SRAI that</srai>
                </srai>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateSRAINode)

        self.assertIsNotNone(ast.children[0].children)
        self.assertEqual(4, len(ast.children[0].children))
        self.assertIsInstance(ast.children[0].children[0], TemplateWordNode)
        self.assertIsInstance(ast.children[0].children[1], TemplateWordNode)
        self.assertIsInstance(ast.children[0].children[2], TemplateWordNode)
        self.assertIsInstance(ast.children[0].children[3], TemplateSRAINode)

        self.assertIsNotNone(ast.children[0].children[3].children)
        self.assertEqual(2, len(ast.children[0].children[3].children))
        self.assertIsInstance(ast.children[0].children[3].children[0], TemplateWordNode)
        self.assertIsInstance(ast.children[0].children[3].children[1], TemplateWordNode)


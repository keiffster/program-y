import unittest
import xml.etree.ElementTree as ET

from programy.parser.template.nodes.thatstar import TemplateThatStarNode

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphThatStarTests(TemplateGraphTestClient):

    def test_thatstar_index_default(self):
        template = ET.fromstring("""
            <template>
                <thatstar />
            </template>
            """)
        root = self._graph.parse_template_expression(template)
        self.assertIsNotNone(root)
        node = root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, TemplateThatStarNode)

        self.assertEqual(root.children[0].to_string(), "[THATSTAR[WORD]1]")

        result = root.resolve_to_string(self.create_client_context("testid"))
        self.assertIsNotNone(result)

    def test_thatstar_index_as_attrib(self):
        template = ET.fromstring("""
            <template>
                <thatstar index="1"></thatstar>
            </template>
            """)
        root = self._graph.parse_template_expression(template)
        self.assertIsNotNone(root)
        node = root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, TemplateThatStarNode)

        self.assertEqual(root.children[0].to_string(), "[THATSTAR[WORD]1]")

        result = root.resolve_to_string(self.create_client_context("testid"))
        self.assertIsNotNone(result)

    def test_thatstar_index_as_child(self):
        template = ET.fromstring("""
            <template>
                <thatstar>
                    <index>1</index>
                </thatstar>
            </template>
            """)
        root = self._graph.parse_template_expression(template)
        self.assertIsNotNone(root)
        node = root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, TemplateThatStarNode)

        self.assertEqual(root.children[0].to_string(), "[THATSTAR[NODE]]")

        result = root.resolve_to_string(self.create_client_context("testid"))
        self.assertIsNotNone(result)

import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.richmedia.list import TemplateListNode

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphListTests(TemplateGraphTestClient):

    def test_list_node_from_xml(self):
        template = ET.fromstring("""
			<template>
				<list>
				    <item>Item1</item>
				    <item>Item2</item>
				</list>
			</template>
			""")
        root = self._graph.parse_template_expression(template)
        self.assertIsNotNone(root)
        self.assertIsInstance(root, TemplateNode)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 1)

        node = root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, TemplateListNode)

        self.assertEqual(2, len(node._items))
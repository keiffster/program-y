import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.richmedia.link import TemplateLinkNode

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphLinkTests(TemplateGraphTestClient):

    def test_link_node_from_xml(self):
        template = ET.fromstring("""
			<template>
				<link>
				    <text>Servusai.com</text>
				    <url>http://www.servusai.com</url>
				</link>
			</template>
			""")
        root = self._graph.parse_template_expression(template)
        self.assertIsNotNone(root)
        self.assertIsInstance(root, TemplateNode)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 1)

        node = root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, TemplateLinkNode)

        self.assertIsNotNone(node._text)
        self.assertIsNotNone(node._url)

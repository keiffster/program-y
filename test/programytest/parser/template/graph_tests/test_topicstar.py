import unittest
import xml.etree.ElementTree as ET

from programy.parser.template.nodes.topicstar import TemplateTopicStarNode

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphTopicStarTests(TemplateGraphTestClient):

    def test_topicstar_index_as_attrib_full(self):
        template = ET.fromstring("""
			<template>
				<topicstar index="1"></topicstar>
			</template>
			""")
        root = self._graph.parse_template_expression(template)
        self.assertIsNotNone(root)
        node = root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, TemplateTopicStarNode)

        self.assertEqual(root.children[0].to_string(), "[TOPICSTAR[WORD]1]")
        self.assertEqual(root.resolve(self._client_context), "*")


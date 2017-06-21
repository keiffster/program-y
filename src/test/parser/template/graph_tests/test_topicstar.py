import unittest
import xml.etree.ElementTree as ET

from programy.parser.template.nodes.topicstar import TemplateTopicStarNode

from test.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphTopicStarTests(TemplateGraphTestClient):

    def test_thatstar_index_as_attrib_full(self):
        template = ET.fromstring("""
			<template>
				<topicstar index="1"></topicstar>
			</template>
			""")
        root = self.parser.parse_template_expression(template)
        self.assertIsNotNone(root)
        node = root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, TemplateTopicStarNode)

        self.assertEqual(root.children[0].to_string(), "TOPICSTAR Index=1")
        self.assertEqual(root.resolve(self.test_bot, self.test_clientid), "*")


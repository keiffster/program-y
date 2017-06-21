import unittest
import xml.etree.ElementTree as ET

from programy.parser.template.nodes.system import TemplateSystemNode

from test.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphSystemTests(TemplateGraphTestClient):

    def test_system_timeout_as_attrib_full(self):
        template = ET.fromstring("""
			<template>
				<system timeout="1000">echo "Hello World"</system>
			</template>
			""")
        root = self.parser.parse_template_expression(template)
        self.assertIsNotNone(root)
        node = root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, TemplateSystemNode)
        self.assertEqual(root.resolve(self.test_bot, self.test_clientid), "Hello World")


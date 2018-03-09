import xml.etree.ElementTree as ET
import os

from programy.parser.template.nodes.system import TemplateSystemNode

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphSystemTests(TemplateGraphTestClient):

    def test_system_timeout_as_attrib_full(self):

        self._client_context.brain.configuration.overrides._allow_system_aiml = True

        template = ET.fromstring("""
			<template>
				<system timeout="1000">echo "Hello World"</system>
			</template>
			""")
        root = self._graph.parse_template_expression(template)
        self.assertIsNotNone(root)
        node = root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, TemplateSystemNode)

        if os.name == 'posix':
            self.assertEqual(root.resolve(self._client_context), "Hello World")
        elif os.name == 'nt':
            self.assertEqual(root.resolve(self._client_context), '"Hello World"')
        else:
            self.assertFalse(True)



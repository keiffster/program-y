import xml.etree.ElementTree as ET
import os

from programy.parser.template.nodes.system import TemplateSystemNode
from programy.parser.template.nodes.word import TemplateWordNode

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphSystemTests(TemplateGraphTestClient):

    def test_system_timeout_as_attrib_full(self):

        self._client_context.brain.configuration.overrides._allow_system_aiml = True

        template = ET.fromstring("""
            <template>
                <system timeout="1000">echo "Hello World"</system>
            </template>
            """)

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        system_node = ast.children[0]
        self.assertIsNotNone(system_node)
        self.assertIsInstance(system_node, TemplateSystemNode)

        self.assertIsInstance(system_node._timeout, TemplateWordNode)

        if os.name == 'posix':
            self.assertEqual(ast.resolve(self._client_context), "Hello World")
        elif os.name == 'nt':
            self.assertEqual(ast.resolve(self._client_context), '"Hello World"')
        else:
            self.assertFalse(True)

    def test_system_timeout_as_attrib_child(self):

        self._client_context.brain.configuration.overrides._allow_system_aiml = True

        template = ET.fromstring("""
            <template>
                <system>
                    <timeout>1000</timeout>
                    echo "Hello World"
                </system>
            </template>
            """)

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        system_node = ast.children[0]
        self.assertIsNotNone(system_node)
        self.assertIsInstance(system_node, TemplateSystemNode)

        if os.name == 'posix':
            self.assertEqual(ast.resolve(self._client_context), "Hello World")
        elif os.name == 'nt':
            self.assertEqual(ast.resolve(self._client_context), '"Hello World"')
        else:
            self.assertFalse(True)


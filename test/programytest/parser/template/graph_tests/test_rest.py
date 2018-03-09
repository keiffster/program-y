import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.rest import TemplateRestNode
from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphRestTests(TemplateGraphTestClient):

    def test_rest(self):
        template = ET.fromstring("""
            <template>
                <rest>one two three four</rest>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        set_node = ast.children[0]
        self.assertIsNotNone(set_node)
        self.assertIsInstance(set_node, TemplateRestNode)

        self.assertIsNotNone(ast)
        self.assertEqual(ast.resolve(self._client_context), "two three four")


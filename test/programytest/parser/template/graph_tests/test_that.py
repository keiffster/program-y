import unittest
import xml.etree.ElementTree as ET

from programy.parser.template.nodes.that import TemplateThatNode

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphThatTests(TemplateGraphTestClient):

    def test_that_index_as_attrib_full(self):
        template = ET.fromstring("""
            <template>
                <that index="1"></that>
            </template>
            """)
        root = self._graph.parse_template_expression(template)
        self.assertIsNotNone(root)
        node = root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, TemplateThatNode)

        self.assertEqual(root.children[0].to_string(), "THAT")


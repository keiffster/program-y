import unittest
import xml.etree.ElementTree as ET

from test.parser.template.graph.test_graph_client import TemplateGraphTestClient


class TemplateGraphTopicTests(TemplateGraphTestClient):


    def test_topicstar_index_as_attrib_full(self):
        template = ET.fromstring("""
			<template>
				<topicstar index="1"></topicstar>
			</template>
			""")
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertEqual(ast.children[0].to_string(), "TOPICSTAR Index=1")
        self.assertEqual(ast.resolve(self.test_bot, self.test_clientid), "*")


if __name__ == '__main__':
    unittest.main()

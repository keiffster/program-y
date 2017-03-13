import unittest
import xml.etree.ElementTree as ET

from programy.parser.template.nodes import *
from test.parser.template.graph.test_graph_client import TemplateGraphTestClient


class TemplateGraphBasicRequestResponseTests(TemplateGraphTestClient):

    def test_response_index_as_attrib_full(self):
        template = ET.fromstring("""
            <template>
                <response index="9"></response>
            </template>
            """)
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)

    def test_request_index_as_attrib_full(self):
        template = ET.fromstring("""
			<template>
				<request index="8"></request>
			</template>
			""")
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)

if __name__ == '__main__':
    unittest.main()

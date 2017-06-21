import unittest
import xml.etree.ElementTree as ET

from test.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphRequestTests(TemplateGraphTestClient):

    def test_request_index_as_attrib_full(self):
        template = ET.fromstring("""
			<template>
				<request index="8"></request>
			</template>
			""")
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)


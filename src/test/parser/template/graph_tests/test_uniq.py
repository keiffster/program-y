import xml.etree.ElementTree as ET

from programy.parser.template.nodes.uniq import TemplateUniqNode

from test.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient

class TemplateGraphUniqTests(TemplateGraphTestClient):

     def test_learnf_simple(self):
        template = ET.fromstring("""
			<template>
			</template>
			""")

        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)

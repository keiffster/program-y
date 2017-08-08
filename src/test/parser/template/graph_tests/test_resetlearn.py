import xml.etree.ElementTree as ET

from programy.parser.template.nodes.resetlearn import TemplateResetLearnNode

from test.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient

class TemplateGraphResetLearnTests(TemplateGraphTestClient):

     def test_learnf_simple(self):
        template = ET.fromstring("""
			<template>
				<resetlearn />
			</template>
			""")

        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)

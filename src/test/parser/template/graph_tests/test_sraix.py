import unittest

import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.sraix import TemplateSRAIXNode

from test.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphSraixTests(TemplateGraphTestClient):

    def test_sraix_template_params_as_attribs(self):
        template = ET.fromstring("""
            <template>
                <sraix host="hostname" botid="testbot" hint="test query" apikey="1234567890" service="ask">
                    Ask this question
                </sraix>
            </template>
            """)
        ast = self.parser.parse_template_expression(template)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateSRAIXNode)
        self.assertEquals("ask", ast.children[0]._service)

    def test_sraix_template_params_as_children(self):
        template = ET.fromstring("""
            <template>
                <sraix>
                    <host>hostname</host>
                    <botid>testbot</botid>
                    <hint>test query</hint>
                    <apikey>1234567890</apikey>
                    <service>ask</service>
                    Ask this question
                </sraix>
            </template>
            """)
        ast = self.parser.parse_template_expression(template)

        ast = self.parser.parse_template_expression(template)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateSRAIXNode)
        self.assertEquals("ask", ast.children[0]._service)

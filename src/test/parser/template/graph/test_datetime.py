import xml.etree.ElementTree as ET
import unittest

from test.parser.template.graph.test_graph_client import TemplateGraphTestClient


class TemplateGraphDateTimeTests(TemplateGraphTestClient):

    def test_date_format_as_attrib(self):
        template = ET.fromstring("""
            <template>
                <date format="%c" />
            </template>
            """)
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsNotNone(ast.resolve(self.test_bot, self.test_clientid))

    def test_date_format_as_attrib_full(self):
        template = ET.fromstring("""
            <template>
                <date format="%c"></date>
            </template>
            """)
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsNotNone(ast.resolve(self.test_bot, self.test_clientid))

    def test_date_format_as_attrib_default(self):
        template = ET.fromstring("""
            <template>
                <date/>
            </template>
            """)
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsNotNone(ast.resolve(self.test_bot, self.test_clientid))

    def test_interval_values_as_attribs(self):
        template = ET.fromstring("""
            <template>
                <interval>
                    <format>%c</format>
                    <style>days</style>
                    <from>Wed Oct  5 16:35:11 2016</from>
                    <to>Fri Oct  7 16:35:11 2016</to>
                </interval>
            </template>
            """)
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertEqual(ast.resolve(self.test_bot, self.test_clientid), "2")

if __name__ == '__main__':
    unittest.main()

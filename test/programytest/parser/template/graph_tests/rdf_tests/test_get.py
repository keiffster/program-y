import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.get import TemplateGetNode
from programy.parser.exceptions import ParserException

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphGetTests(TemplateGraphTestClient):

    def test_tuples_single_var_single_result(self):

        self.test_bot.brain.rdf.add_entity("MONKEY", "LEGS", "2")
        self.test_bot.brain.rdf.add_entity("MONKEY", "HASFUR", "true")
        self.test_bot.brain.rdf.add_entity("ZEBRA", "LEGS", "4")
        self.test_bot.brain.rdf.add_entity("ELEPHANT", "TRUNK", "true")

        template = ET.fromstring("""
			<template>
				<get var="?x">
				    <tuple> 
				        <select>
                            <vars>?x</vars>
                            <q><subj>?x</subj><pred>LEGS</pred><obj>2</obj></q>
                        </select>
				    </tuple>
				</get>
			</template>
			""")
        self.assertIsNotNone(template)

        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)

        result = ast.resolve(self.test_bot, self.test_clientid)
        self.assertIsNotNone(result)
        self.assertEquals("MONKEY", result)

    def test_tuples_multi_vars_single_results(self):
        self.test_bot.brain.rdf.add_entity("MONKEY", "LEGS", "2")
        self.test_bot.brain.rdf.add_entity("MONKEY", "HASFUR", "true")
        self.test_bot.brain.rdf.add_entity("ZEBRA", "LEGS", "4")
        self.test_bot.brain.rdf.add_entity("ELEPHANT", "TRUNK", "true")

        template = ET.fromstring("""
            <template>
                <get var="?x ?y">
                    <tuple> 
                        <select>
                            <vars>?x ?y</vars>
                            <q><subj>?x</subj><pred>?y</pred><obj>2</obj></q>
                        </select>
                    </tuple>
                </get>
            </template>
            """)
        self.assertIsNotNone(template)

        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)

        result = ast.resolve(self.test_bot, self.test_clientid)
        self.assertIsNotNone(result)
        self.assertEquals("MONKEY LEGS", result)

    def test_tuples_single_var_multi_resultss(self):

        self.test_bot.brain.rdf.add_entity("MONKEY", "LEGS", "2")
        self.test_bot.brain.rdf.add_entity("MONKEY", "HASFUR", "true")
        self.test_bot.brain.rdf.add_entity("ZEBRA", "LEGS", "4")
        self.test_bot.brain.rdf.add_entity("BIRD", "LEGS", "2")
        self.test_bot.brain.rdf.add_entity("ELEPHANT", "TRUNK", "true")

        template = ET.fromstring("""
			<template>
				<get var="?x">
				    <tuple> 
				        <select>
                            <vars>?x</vars>
                            <q><subj>?x</subj><pred>LEGS</pred><obj>2</obj></q>
                        </select>
				    </tuple>
				</get>
			</template>
			""")
        self.assertIsNotNone(template)

        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)

        result = ast.resolve(self.test_bot, self.test_clientid)
        self.assertIsNotNone(result)
        self.assertEquals("MONKEY BIRD", result)

    def test_tuples_multi_vars_multi_resultss(self):

        self.test_bot.brain.rdf.add_entity("MONKEY", "LEGS", "2")
        self.test_bot.brain.rdf.add_entity("MONKEY", "HASFUR", "true")
        self.test_bot.brain.rdf.add_entity("ZEBRA", "LEGS", "4")
        self.test_bot.brain.rdf.add_entity("BIRD", "LEGS", "2")
        self.test_bot.brain.rdf.add_entity("ELEPHANT", "TRUNK", "true")

        template = ET.fromstring("""
			<template>
				<get var="?x ?y">
				    <tuple> 
				        <select>
                            <vars>?x ?y</vars>
                            <q><subj>?x</subj><pred>?y</pred><obj>2</obj></q>
                        </select>
				    </tuple>
				</get>
			</template>
			""")
        self.assertIsNotNone(template)

        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)

        result = ast.resolve(self.test_bot, self.test_clientid)
        self.assertIsNotNone(result)
        self.assertEquals("MONKEY LEGS BIRD LEGS", result)
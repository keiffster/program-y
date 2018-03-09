import xml.etree.ElementTree as ET

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphFirstTests(TemplateGraphTestClient):

    def test_first_single_var_single_result(self):

        self._client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2")
        self._client_context.brain.rdf.add_entity("MONKEY", "HASFUR", "true")
        self._client_context.brain.rdf.add_entity("ZEBRA", "LEGS", "4")
        self._client_context.brain.rdf.add_entity("ELEPHANT", "TRUNK", "true")

        template = ET.fromstring("""
			<template>
               <first>
                    <select>
                        <vars>?x</vars>
                        <q>
                            <subj>?x</subj>
                            <pred>HASFUR</pred>
                            <obj>true</obj>
                        </q>
                    </select>
                </first>
			</template>
			""")
        self.assertIsNotNone(template)

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEquals('[["?x", "MONKEY"]]', result)

    def test_first_single_var_multipe_result(self):

        self._client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2")
        self._client_context.brain.rdf.add_entity("MONKEY", "HASFUR", "true")
        self._client_context.brain.rdf.add_entity("ZEBRA", "LEGS", "4")
        self._client_context.brain.rdf.add_entity("BIRD", "LEGS", "2")
        self._client_context.brain.rdf.add_entity("ELEPHANT", "TRUNK", "true")

        template = ET.fromstring("""
			<template>
               <first>
                    <select>
                        <vars>?x</vars>
                        <q>
                            <subj>?x</subj>
                            <pred>LEGS</pred>
                            <obj>2</obj>
                        </q>
                    </select>
                </first>
			</template>
			""")
        self.assertIsNotNone(template)

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEquals('[["?x", "MONKEY"]]', result)

    def test_first_multi_var_single_result(self):

        self._client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2")
        self._client_context.brain.rdf.add_entity("MONKEY", "HASFUR", "true")
        self._client_context.brain.rdf.add_entity("ZEBRA", "LEGS", "4")
        self._client_context.brain.rdf.add_entity("ELEPHANT", "TRUNK", "true")

        template = ET.fromstring("""
			<template>
               <first>
                    <select>
                        <vars>?x</vars>
                        <q>
                            <subj>?x</subj>
                            <pred>HASFUR</pred>
                            <obj>?y</obj>
                        </q>
                    </select>
                </first>
			</template>
			""")
        self.assertIsNotNone(template)

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEquals('[["?x", "MONKEY"], ["?y", "true"]]', result)

    def test_first_multiple_var_multipe_result(self):

        self._client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2")
        self._client_context.brain.rdf.add_entity("MONKEY", "HASFUR", "true")
        self._client_context.brain.rdf.add_entity("ZEBRA", "LEGS", "4")
        self._client_context.brain.rdf.add_entity("BIRD", "LEGS", "2")
        self._client_context.brain.rdf.add_entity("ELEPHANT", "TRUNK", "true")

        template = ET.fromstring("""
			<template>
               <first>
                    <select>
                        <vars>?x</vars>
                        <q>
                            <subj>?x</subj>
                            <pred>LEGS</pred>
                            <obj>?y</obj>
                        </q>
                    </select>
                </first>
			</template>
			""")
        self.assertIsNotNone(template)

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEquals('[["?x", "MONKEY"], ["?y", "2"]]', result)

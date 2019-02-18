import xml.etree.ElementTree as ET

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphFirstTests(TemplateGraphTestClient):

    def test_rest_single_var_single_result(self):

        self._client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("MONKEY", "HASFUR", "true", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ZEBRA", "LEGS", "4", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ELEPHANT", "TRUNK", "true", "ANIMALS")

        template = ET.fromstring("""
			<template>
               <rest>
                    <select>
                        <vars>?x</vars>
                        <q>
                            <subj>?x</subj>
                            <pred>HASFUR</pred>
                            <obj>true</obj>
                        </q>
                    </select>
                </rest>
			</template>
			""")
        self.assertIsNotNone(template)

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual('NIL', result)

    def test_rest_single_var_multipe_result(self):

        self._client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("MONKEY", "HASFUR", "true", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ZEBRA", "LEGS", "4", "ANIMALS")
        self._client_context.brain.rdf.add_entity("BIRD", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ELEPHANT", "TRUNK", "true", "ANIMALS")

        template = ET.fromstring("""
			<template>
               <rest>
                    <select>
                        <vars>?x</vars>
                        <q>
                            <subj>?x</subj>
                            <pred>LEGS</pred>
                            <obj>2</obj>
                        </q>
                    </select>
                </rest>
			</template>
			""")
        self.assertIsNotNone(template)

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual('[[["?x", "BIRD"]]]', result)

    def test_rest_multi_var_single_result(self):

        self._client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("MONKEY", "HASFUR", "true", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ZEBRA", "LEGS", "4", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ELEPHANT", "TRUNK", "true", "ANIMALS")

        template = ET.fromstring("""
			<template>
               <rest>
                    <select>
                        <vars>?x</vars>
                        <q>
                            <subj>?x</subj>
                            <pred>HASFUR</pred>
                            <obj>?y</obj>
                        </q>
                    </select>
                </rest>
			</template>
			""")
        self.assertIsNotNone(template)

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual('NIL', result)

    def test_rest_multiple_var_multipe_result(self):

        self._client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("MONKEY", "HASFUR", "true", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ZEBRA", "LEGS", "4", "ANIMALS")
        self._client_context.brain.rdf.add_entity("BIRD", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ELEPHANT", "TRUNK", "true", "ANIMALS")

        template = ET.fromstring("""
			<template>
               <rest>
                    <select>
                        <vars>?x</vars>
                        <q>
                            <subj>?x</subj>
                            <pred>LEGS</pred>
                            <obj>?y</obj>
                        </q>
                    </select>
                </rest>
			</template>
			""")
        self.assertIsNotNone(template)

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual('[[["?x", "ZEBRA"], ["?y", "4"]], [["?x", "BIRD"], ["?y", "2"]]]', result)

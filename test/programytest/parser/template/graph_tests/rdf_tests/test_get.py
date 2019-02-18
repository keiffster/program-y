import xml.etree.ElementTree as ET

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphGetTests(TemplateGraphTestClient):

    def test_tuples_single_var_single_result(self):

        self._client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("MONKEY", "HASFUR", "true", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ZEBRA", "LEGS", "4", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ELEPHANT", "TRUNK", "true", "ANIMALS")

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

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("MONKEY", result)

    def test_tuples_multi_vars_single_results(self):
        self._client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("MONKEY", "HASFUR", "true", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ZEBRA", "LEGS", "4", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ELEPHANT", "TRUNK", "true", "ANIMALS")

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

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("MONKEY LEGS", result)

    def test_tuples_single_var_multi_resultss(self):

        self._client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("MONKEY", "HASFUR", "true", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ZEBRA", "LEGS", "4", "ANIMALS")
        self._client_context.brain.rdf.add_entity("BIRD", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ELEPHANT", "TRUNK", "true", "ANIMALS")

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

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("MONKEY BIRD", result)

    def test_tuples_multi_vars_multi_resultss(self):

        self._client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2", "ANIMALS", "ANIMALS")
        self._client_context.brain.rdf.add_entity("MONKEY", "HASFUR", "true", "ANIMALS", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ZEBRA", "LEGS", "4", "ANIMALS", "ANIMALS")
        self._client_context.brain.rdf.add_entity("BIRD", "LEGS", "2", "ANIMALS", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ELEPHANT", "TRUNK", "true", "ANIMALS", "ANIMALS")

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

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("MONKEY LEGS BIRD LEGS", result)

    def test_get_from_tuple_from_get_from_var(self):
        template = ET.fromstring("""
        			<template>
        			    <think>
        			        <set var="head">[["?x", "TEST1"]]</set>
        			    </think>
        				<get var="?x">
        				    <tuple> 
        				        <get var="head"/>
        				    </tuple>
        				</get>
        			</template>
        			""")
        self.assertIsNotNone(template)

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("TEST1", result)

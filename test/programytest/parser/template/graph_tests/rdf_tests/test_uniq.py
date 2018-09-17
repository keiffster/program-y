import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.uniq import TemplateUniqNode

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient

class TemplateGraphUniqTests(TemplateGraphTestClient):

    def test_uniq_type1(self):
        template = ET.fromstring("""
     			<template>
     			    <uniq>
     			        <subj>X</subj>
     			        <pred>Y</pred>
     			        <obj>Z</obj>
     			    </uniq>
     			</template>
     			""")

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateUniqNode)
        self.assertEqual(0, len(ast.children[0].children))

    def test_uniq_query_on_object(self):
        self._client_context.brain.rdf.add_entity("MONKEY", "legs", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("MONKEY", "hasFur", "true", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ZEBRA", "legs", "4", "ANIMALS")
        self._client_context.brain.rdf.add_entity("BIRD", "legs", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ELEPHANT", "trunk", "true", "ANIMALS")

        template = ET.fromstring("""
     			<template>
     			    <uniq>
     			        <subj>MONKEY</subj>
     			        <pred>legs</pred>
     			        <obj>?legs</obj>
     			    </uniq>
     			</template>
     			""")

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("2", result)

    def test_uniq_query_on_subject(self):
        self._client_context.brain.rdf.add_entity("MONKEY", "legs", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("MONKEY", "hasFur", "true", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ZEBRA", "legs", "4", "ANIMALS")
        self._client_context.brain.rdf.add_entity("BIRD", "legs", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ELEPHANT", "trunk", "true", "ANIMALS")

        template = ET.fromstring("""
     			<template>
     			    <uniq>
     			        <subj>?animal</subj>
     			        <pred>legs</pred>
     			        <obj>2</obj>
     			    </uniq>
     			</template>
     			""")

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("MONKEY BIRD", result)

    def test_uniq_query_on_predicate(self):
        self._client_context.brain.rdf.add_entity("MONKEY", "legs", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("MONKEY", "hasFur", "true", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ZEBRA", "legs", "4", "ANIMALS")
        self._client_context.brain.rdf.add_entity("BIRD", "legs", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ELEPHANT", "trunk", "true", "ANIMALS")

        template = ET.fromstring("""
     			<template>
     			    <uniq>
     			        <subj>MONKEY</subj>
     			        <pred>?hasLegs</pred>
     			        <obj>2</obj>
     			    </uniq>
     			</template>
     			""")

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("LEGS", result)
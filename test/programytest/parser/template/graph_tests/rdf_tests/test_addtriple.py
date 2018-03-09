import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.addtriple import TemplateAddTripleNode

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphAddTripleTests(TemplateGraphTestClient):

    def test_add_triple_type1(self):
        template = ET.fromstring("""
			<template>
			    <addtriple>
			        <subj>X</subj>
			        <pred>Y</pred>
			        <obj>Z</obj>
			    </addtriple>
			</template>
			""")

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateAddTripleNode)
        self.assertEqual(0, len(ast.children[0].children))

        self.assertFalse(self._client_context.brain.rdf.has_object("X", "Y", "Z"))
        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertTrue(self._client_context.brain.rdf.has_object("X", "Y", "Z"))

    def test_add_triple_type2(self):
        template = ET.fromstring("""
			<template>
			    <addtriple subj="X" pred="Y" obj="Z">
			    </addtriple>
			</template>
			""")

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateAddTripleNode)
        self.assertEqual(0, len(ast.children[0].children))

        self.assertFalse(self._client_context.brain.rdf.has_object("X", "Y", "Z"))
        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertTrue(self._client_context.brain.rdf.has_object("X", "Y", "Z"))

    def test_add_triple_type3(self):
        template = ET.fromstring("""
			<template>
			    <addtriple subj="X" pred="Y" obj="Z" />
			</template>
			""")

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateAddTripleNode)
        self.assertEqual(0, len(ast.children[0].children))

        self.assertFalse(self._client_context.brain.rdf.has_object("X", "Y", "Z"))
        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertTrue(self._client_context.brain.rdf.has_object("X", "Y", "Z"))

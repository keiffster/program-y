import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.deletetriple import TemplateDeleteTripleNode

from test.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphDeleteTripleTests(TemplateGraphTestClient):

    def test_delete_triple_type1(self):
        self.assertFalse(self.test_bot.brain.rdf.has_object("X", "Y", "Z"))
        self.test_bot.brain.rdf.add_entity("X", "Y", "Z")
        self.assertTrue(self.test_bot.brain.rdf.has_object("X", "Y", "Z"))

        template = ET.fromstring("""
			<template>
			    <deletetriple>
			        <subj>X</subj>
			        <pred>Y</pred>
			        <obj>Z</obj>
			    </deletetriple>
			</template>
			""")

        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateDeleteTripleNode)
        self.assertEqual(0, len(ast.children[0].children))

        result = ast.resolve(self.test_bot, self.test_clientid)
        self.assertIsNotNone(result)
        self.assertFalse(self.test_bot.brain.rdf.has_object("X", "Y", "Z"))

    def test_delete_triple_type2(self):
        self.assertFalse(self.test_bot.brain.rdf.has_object("X", "Y", "Z"))
        self.test_bot.brain.rdf.add_entity("X", "Y", "Z")
        self.assertTrue(self.test_bot.brain.rdf.has_object("X", "Y", "Z"))

        template = ET.fromstring("""
			<template>
			    <deletetriple subj="X" pred="Y" obj="Z">
			    </deletetriple>
			</template>
			""")

        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateDeleteTripleNode)
        self.assertEqual(0, len(ast.children[0].children))

        result = ast.resolve(self.test_bot, self.test_clientid)
        self.assertIsNotNone(result)
        self.assertFalse(self.test_bot.brain.rdf.has_object("X", "Y", "Z"))

    def test_delete_triple_type3(self):
        self.assertFalse(self.test_bot.brain.rdf.has_object("X", "Y", "Z"))
        self.test_bot.brain.rdf.add_entity("X", "Y", "Z")
        self.assertTrue(self.test_bot.brain.rdf.has_object("X", "Y", "Z"))

        template = ET.fromstring("""
			<template>
			    <deletetriple subj="X" pred="Y" obj="Z" />
			</template>
			""")

        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateDeleteTripleNode)
        self.assertEqual(0, len(ast.children[0].children))

        result = ast.resolve(self.test_bot, self.test_clientid)
        self.assertIsNotNone(result)
        self.assertFalse(self.test_bot.brain.rdf.has_object("X", "Y", "Z"))

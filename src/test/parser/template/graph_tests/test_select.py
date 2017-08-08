import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.select import TemplateSelectNode

from test.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphSelectTests(TemplateGraphTestClient):

     def test_select_single_vars_single_query(self):
        template = ET.fromstring("""
			<template>
			    <select>
			        <vars>?x</vars>
			        <q><subj>X</subj><pred>Y</pred><obj>Z</obj></q>
			    </select>
			</template>
			""")

        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateSelectNode)
        self.assertEqual(0, len(ast.children[0].children))

        self.assertEquals(1, len(ast.children[0]._vars))
        self.assertEquals(1, len(ast.children[0]._queries))

     def test_select_multi_vars_single_query(self):
        template = ET.fromstring("""
			<template>
			    <select>
			        <vars>?x ?y</vars>
			        <q><subj>X</subj><pred>Y</pred><obj>Z</obj></q>
			    </select>
			</template>
			""")

        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateSelectNode)
        self.assertEqual(0, len(ast.children[0].children))

        self.assertEquals(2, len(ast.children[0]._vars))
        self.assertEquals(1, len(ast.children[0]._queries))


     def test_select_single_vars_multie_query(self):
        template = ET.fromstring("""
			<template>
			    <select>
			        <vars>?x</vars>
			        <q><subj>A</subj><pred>B</pred><obj>C</obj></q>
			        <q><subj>X</subj><pred>Y</pred><obj>Z</obj></q>
			    </select>
			</template>
			""")

        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateSelectNode)
        self.assertEqual(0, len(ast.children[0].children))

        self.assertEquals(1, len(ast.children[0]._vars))
        self.assertEquals(2, len(ast.children[0]._queries))


     def test_select_multi_vars_multi_query(self):
        template = ET.fromstring("""
			<template>
			    <select>
			        <vars>?x ?y</vars>
			        <q><subj>A</subj><pred>B</pred><obj>C</obj></q>
			        <q><subj>X</subj><pred>Y</pred><obj>Z</obj></q>
			    </select>
			</template>
			""")

        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateSelectNode)
        self.assertEqual(0, len(ast.children[0].children))

        self.assertEquals(2, len(ast.children[0]._vars))
        self.assertEquals(2, len(ast.children[0]._queries))

     def test_select_single_vars_mixed_query(self):
        template = ET.fromstring("""
			<template>
			    <select>
			        <vars>?x</vars>
			        <q><subj>A</subj><pred>B</pred><obj>C</obj></q>
			        <notq><subj>X</subj><pred>Y</pred><obj>Z</obj></notq>
			    </select>
			</template>
			""")

        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateSelectNode)
        self.assertEqual(0, len(ast.children[0].children))

        self.assertEquals(1, len(ast.children[0]._vars))
        self.assertEquals(2, len(ast.children[0]._queries))

     def test_select_multi_vars_mixed_query(self):
        template = ET.fromstring("""
			<template>
			    <select>
			        <vars>?x ?y</vars>
			        <q><subj>A</subj><pred>B</pred><obj>C</obj></q>
			        <notq><subj>X</subj><pred>Y</pred><obj>Z</obj></notq>
			    </select>
			</template>
			""")

        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateSelectNode)
        self.assertEqual(0, len(ast.children[0].children))

        self.assertEquals(2, len(ast.children[0]._vars))
        self.assertEquals(2, len(ast.children[0]._queries))


     def test_select_no_vars_single_query(self):
        template = ET.fromstring("""
			<template>
			    <select>
			        <q><subj>A</subj><pred>B</pred><obj>C</obj></q>
			    </select>
			</template>
			""")

        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateSelectNode)
        self.assertEqual(0, len(ast.children[0].children))

        self.assertEquals(0, len(ast.children[0]._vars))
        self.assertEquals(1, len(ast.children[0]._queries))


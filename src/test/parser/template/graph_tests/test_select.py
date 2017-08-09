import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.template.nodes.select import TemplateSelectNode

from test.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphSelectTests(TemplateGraphTestClient):
    def test_select_single_vars_single_query(self):
        template = ET.fromstring("""
			<template>
			    <select>
			        <vars>?x</vars>
			        <q><subj>?x</subj><pred>Y</pred><obj>Z</obj></q>
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
        self.assertTrue("?x" in ast.children[0]._vars)

        self.assertEquals(1, len(ast.children[0]._queries))
        query1 = ast.children[0]._queries[0]
        self.assertEquals("q", query1._type)
        self.assertIsInstance(query1._subj, TemplateNode)
        self.assertEquals(1, len(query1._subj.children))
        self.assertIsInstance(query1._subj.children[0], TemplateWordNode)
        self.assertEquals("?x", query1._subj.resolve(None, None))
        self.assertIsInstance(query1._pred, TemplateNode)
        self.assertEquals("Y", query1._pred.resolve(None, None))
        self.assertIsInstance(query1._obj, TemplateNode)
        self.assertEquals("Z", query1._obj.resolve(None, None))

    def test_select_multi_vars_single_query(self):
        template = ET.fromstring("""
			<template>
			    <select>
			        <vars>?x ?y</vars>
			        <q><subj>?x</subj><pred>?y</pred><obj>Z</obj></q>
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
        self.assertTrue("?x" in ast.children[0]._vars)
        self.assertTrue("?y" in ast.children[0]._vars)

        self.assertEquals(1, len(ast.children[0]._queries))
        query1 = ast.children[0]._queries[0]
        self.assertEquals("q", query1._type)
        self.assertIsInstance(query1._subj, TemplateNode)
        self.assertEquals(1, len(query1._subj.children))
        self.assertIsInstance(query1._subj.children[0], TemplateWordNode)
        self.assertEquals("?x", query1._subj.resolve(None, None))
        self.assertIsInstance(query1._pred, TemplateNode)
        self.assertEquals("?y", query1._pred.resolve(None, None))
        self.assertIsInstance(query1._obj, TemplateNode)
        self.assertEquals("Z", query1._obj.resolve(None, None))

    def test_select_single_vars_multie_query(self):
        template = ET.fromstring("""
			<template>
			    <select>
			        <vars>?x</vars>
			        <q><subj>A</subj><pred>B</pred><obj>C</obj></q>
			        <q><subj>?x</subj><pred>Y</pred><obj>Z</obj></q>
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
        self.assertTrue("?x" in ast.children[0]._vars)

        self.assertEquals(2, len(ast.children[0]._queries))

        query1 = ast.children[0]._queries[0]
        self.assertEquals("q", query1._type)
        self.assertIsInstance(query1._subj, TemplateNode)
        self.assertEquals(1, len(query1._subj.children))
        self.assertIsInstance(query1._subj.children[0], TemplateWordNode)
        self.assertEquals("A", query1._subj.resolve(None, None))
        self.assertIsInstance(query1._pred, TemplateNode)
        self.assertEquals("B", query1._pred.resolve(None, None))
        self.assertIsInstance(query1._obj, TemplateNode)
        self.assertEquals("C", query1._obj.resolve(None, None))

        query2 = ast.children[0]._queries[1]
        self.assertEquals("q", query2._type)
        self.assertIsInstance(query2._subj, TemplateNode)
        self.assertEquals(1, len(query2._subj.children))
        self.assertIsInstance(query2._subj.children[0], TemplateWordNode)
        self.assertEquals("?x", query2._subj.resolve(None, None))
        self.assertIsInstance(query2._pred, TemplateNode)
        self.assertEquals("Y", query2._pred.resolve(None, None))
        self.assertIsInstance(query2._obj, TemplateNode)
        self.assertEquals("Z", query2._obj.resolve(None, None))

    def test_select_multi_vars_multi_query(self):
        template = ET.fromstring("""
			<template>
			    <select>
			        <vars>?x ?y</vars>
			        <q><subj>A</subj><pred>B</pred><obj>C</obj></q>
			        <q><subj>?x</subj><pred>?y</pred><obj>Z</obj></q>
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
        self.assertTrue("?x" in ast.children[0]._vars)
        self.assertTrue("?y" in ast.children[0]._vars)

        self.assertEquals(2, len(ast.children[0]._queries))

        query1 = ast.children[0]._queries[0]
        self.assertEquals("q", query1._type)
        self.assertIsInstance(query1._subj, TemplateNode)
        self.assertEquals(1, len(query1._subj.children))
        self.assertIsInstance(query1._subj.children[0], TemplateWordNode)
        self.assertEquals("A", query1._subj.resolve(None, None))
        self.assertIsInstance(query1._pred, TemplateNode)
        self.assertEquals("B", query1._pred.resolve(None, None))
        self.assertIsInstance(query1._obj, TemplateNode)
        self.assertEquals("C", query1._obj.resolve(None, None))

        query2 = ast.children[0]._queries[1]
        self.assertEquals("q", query2._type)
        self.assertIsInstance(query2._subj, TemplateNode)
        self.assertEquals(1, len(query2._subj.children))
        self.assertIsInstance(query2._subj.children[0], TemplateWordNode)
        self.assertEquals("?x", query2._subj.resolve(None, None))
        self.assertIsInstance(query2._pred, TemplateNode)
        self.assertEquals("?y", query2._pred.resolve(None, None))
        self.assertIsInstance(query2._obj, TemplateNode)
        self.assertEquals("Z", query2._obj.resolve(None, None))

    def test_select_single_vars_mixed_query(self):
        template = ET.fromstring("""
			<template>
			    <select>
			        <vars>?x</vars>
			        <q><subj>A</subj><pred>B</pred><obj>C</obj></q>
			        <notq><subj>?x</subj><pred>?x</pred><obj>Z</obj></notq>
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
        self.assertTrue("?x" in ast.children[0]._vars)

        self.assertEquals(2, len(ast.children[0]._queries))

        query1 = ast.children[0]._queries[0]
        self.assertEquals("q", query1._type)
        self.assertIsInstance(query1._subj, TemplateNode)
        self.assertEquals(1, len(query1._subj.children))
        self.assertIsInstance(query1._subj.children[0], TemplateWordNode)
        self.assertEquals("A", query1._subj.resolve(None, None))
        self.assertIsInstance(query1._pred, TemplateNode)
        self.assertEquals("B", query1._pred.resolve(None, None))
        self.assertIsInstance(query1._obj, TemplateNode)
        self.assertEquals("C", query1._obj.resolve(None, None))

        query2 = ast.children[0]._queries[1]
        self.assertEquals("notq", query2._type)
        self.assertIsInstance(query2._subj, TemplateNode)
        self.assertEquals(1, len(query2._subj.children))
        self.assertIsInstance(query2._subj.children[0], TemplateWordNode)
        self.assertEquals("?x", query2._subj.resolve(None, None))
        self.assertIsInstance(query2._pred, TemplateNode)
        self.assertEquals("?x", query2._pred.resolve(None, None))
        self.assertIsInstance(query2._obj, TemplateNode)
        self.assertEquals("Z", query2._obj.resolve(None, None))

    def test_select_multi_vars_mixed_query(self):
        template = ET.fromstring("""
			<template>
			    <select>
			        <vars>?A ?X</vars>
			        <q><subj>?A</subj><pred>B</pred><obj>C</obj></q>
			        <notq><subj>?X</subj><pred>Y</pred><obj>Z</obj></notq>
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
        self.assertTrue("?A" in ast.children[0]._vars)
        self.assertTrue("?X" in ast.children[0]._vars)

        self.assertEquals(2, len(ast.children[0]._queries))

        query1 = ast.children[0]._queries[0]
        self.assertEquals("q", query1._type)
        self.assertIsInstance(query1._subj, TemplateNode)
        self.assertEquals(1, len(query1._subj.children))
        self.assertIsInstance(query1._subj.children[0], TemplateWordNode)
        self.assertEquals("?A", query1._subj.resolve(None, None))
        self.assertIsInstance(query1._pred, TemplateNode)
        self.assertEquals("B", query1._pred.resolve(None, None))
        self.assertIsInstance(query1._obj, TemplateNode)
        self.assertEquals("C", query1._obj.resolve(None, None))

        query2 = ast.children[0]._queries[1]
        self.assertEquals("notq", query2._type)
        self.assertIsInstance(query2._subj, TemplateNode)
        self.assertEquals(1, len(query2._subj.children))
        self.assertIsInstance(query2._subj.children[0], TemplateWordNode)
        self.assertEquals("?X", query2._subj.resolve(None, None))
        self.assertIsInstance(query2._pred, TemplateNode)
        self.assertEquals("Y", query2._pred.resolve(None, None))
        self.assertIsInstance(query2._obj, TemplateNode)
        self.assertEquals("Z", query2._obj.resolve(None, None))


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

        query1 = ast.children[0]._queries[0]
        self.assertEquals("q", query1._type)
        self.assertIsInstance(query1._subj, TemplateNode)
        self.assertEquals(1, len(query1._subj.children))
        self.assertIsInstance(query1._subj.children[0], TemplateWordNode)
        self.assertEquals("A", query1._subj.resolve(None, None))
        self.assertIsInstance(query1._pred, TemplateNode)
        self.assertEquals("B", query1._pred.resolve(None, None))
        self.assertIsInstance(query1._obj, TemplateNode)
        self.assertEquals("C", query1._obj.resolve(None, None))

    def test_query_no_vars(self):
        self.test_bot.brain.triples.add_triple("MONKEY", "legs", "2")
        self.test_bot.brain.triples.add_triple("MONKEY", "hasFur", "true")
        self.test_bot.brain.triples.add_triple("ZEBRA", "legs", "4")
        self.test_bot.brain.triples.add_triple("BIRD", "legs", "2")
        self.test_bot.brain.triples.add_triple("ELEPHANT", "trunk", "true")

        template = ET.fromstring("""
                <template>
                    <select>
                        <q><subj>MONKEY</subj><pred>legs</pred><obj>2</obj></q>
                    </select>
                </template>
                """)

        ast = self.parser.parse_template_expression(template)

        result = ast.resolve(self.test_bot, self.test_clientid)
        self.assertIsNotNone(result)
        self.assertEquals("(MONKEY, legs, 2)", result)

    def test_query_var(self):
        self.test_bot.brain.triples.add_triple("MONKEY", "legs", "2")
        self.test_bot.brain.triples.add_triple("MONKEY", "hasFur", "true")
        self.test_bot.brain.triples.add_triple("ZEBRA", "legs", "4")
        self.test_bot.brain.triples.add_triple("BIRD", "legs", "2")
        self.test_bot.brain.triples.add_triple("ELEPHANT", "trunk", "true")

        template = ET.fromstring("""
                <template>
                    <select>
                        <vars>?x</vars>
                        <q><subj>?x</subj><pred>legs</pred><obj>2</obj></q>
                    </select>
                </template>
                """)

        ast = self.parser.parse_template_expression(template)

        result = ast.resolve(self.test_bot, self.test_clientid)
        self.assertIsNotNone(result)
        self.assertEquals("(MONKEY)(BIRD)", result)

    def test_query_multi_vars(self):
        self.test_bot.brain.triples.add_triple("MONKEY", "legs", "2")
        self.test_bot.brain.triples.add_triple("MONKEY", "hasFur", "true")
        self.test_bot.brain.triples.add_triple("ZEBRA", "legs", "4")
        self.test_bot.brain.triples.add_triple("BIRD", "legs", "2")
        self.test_bot.brain.triples.add_triple("ELEPHANT", "trunk", "true")

        template = ET.fromstring("""
                <template>
                    <select>
                        <vars>?x ?y</vars>
                        <q><subj>?x</subj><pred>?y</pred><obj>2</obj></q>
                    </select>
                </template>
                """)

        ast = self.parser.parse_template_expression(template)

        result = ast.resolve(self.test_bot, self.test_clientid)
        self.assertIsNotNone(result)
        self.assertEquals("(MONKEY, legs)(BIRD, legs)", result)

    def test_query_var_multi_queries(self):
        self.test_bot.brain.triples.add_triple("MONKEY", "legs", "2")
        self.test_bot.brain.triples.add_triple("MONKEY", "hasFur", "true")
        self.test_bot.brain.triples.add_triple("ZEBRA", "legs", "4")
        self.test_bot.brain.triples.add_triple("BIRD", "legs", "2")
        self.test_bot.brain.triples.add_triple("ELEPHANT", "trunk", "true")

        template = ET.fromstring("""
                <template>
                    <select>
                        <vars>?x</vars>
                        <q><subj>?x</subj><pred>legs</pred><obj>2</obj></q>
                        <q><subj>?x</subj><pred>hasFur</pred><obj>true</obj></q>
                    </select>
                </template>
                """)

        ast = self.parser.parse_template_expression(template)

        result = ast.resolve(self.test_bot, self.test_clientid)
        self.assertIsNotNone(result)
        self.assertEquals("(MONKEY)", result)

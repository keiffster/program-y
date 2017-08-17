import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.template.nodes.select import TemplateSelectNode
from programy.rdf.query import RDFQuery
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

        select_node = ast.children[0]
        self.assertIsNotNone(select_node.query)
        self.assertIsNotNone(select_node.query.vars)
        self.assertEquals(1, len(select_node.query.vars))
        self.assertTrue("?x" in select_node.query.vars)

        self.assertEquals(1, len(select_node.query.queries))
        query1 = select_node.query.queries[0]
        self.assertEquals(RDFQuery.QUERY, query1.query_type)
        self.assertIsInstance(query1.subject, TemplateNode)
        self.assertEquals(1, len(query1.subject.children))
        self.assertIsInstance(query1.subject.children[0], TemplateWordNode)
        self.assertEquals("?x", query1.subject.resolve(None, None))
        self.assertIsInstance(query1.predicate, TemplateNode)
        self.assertEquals("Y", query1.predicate.resolve(None, None))
        self.assertIsInstance(query1.object, TemplateNode)
        self.assertEquals("Z", query1.object.resolve(None, None))

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

        select_node = ast.children[0]
        self.assertIsNotNone(select_node.query)
        self.assertIsNotNone(select_node.query.vars)
        self.assertEquals(2, len(select_node.query.vars))
        self.assertTrue("?x" in select_node.query.vars)
        self.assertTrue("?y" in select_node.query.vars)

        self.assertEquals(1, len(select_node.query.queries))
        query1 = select_node.query.queries[0]
        self.assertEquals(RDFQuery.QUERY, query1.query_type)
        self.assertIsInstance(query1.subject, TemplateNode)
        self.assertEquals(1, len(query1.subject.children))
        self.assertIsInstance(query1.subject.children[0], TemplateWordNode)
        self.assertEquals("?x", query1.subject.resolve(None, None))
        self.assertIsInstance(query1.predicate, TemplateNode)
        self.assertEquals("?y", query1.predicate.resolve(None, None))
        self.assertIsInstance(query1.object, TemplateNode)
        self.assertEquals("Z", query1.object.resolve(None, None))

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

        select_node = ast.children[0]
        self.assertIsNotNone(select_node.query)
        self.assertIsNotNone(select_node.query.vars)
        self.assertEquals(1, len(select_node.query.vars))
        self.assertTrue("?x" in select_node.query.vars)

        self.assertEquals(2, len(select_node.query.queries))

        query1 = select_node.query.queries[0]
        self.assertEquals(RDFQuery.QUERY, query1.query_type)
        self.assertIsInstance(query1.subject, TemplateNode)
        self.assertEquals(1, len(query1.subject.children))
        self.assertIsInstance(query1.subject.children[0], TemplateWordNode)
        self.assertEquals("A", query1.subject.resolve(None, None))
        self.assertIsInstance(query1.predicate, TemplateNode)
        self.assertEquals("B", query1.predicate.resolve(None, None))
        self.assertIsInstance(query1.object, TemplateNode)
        self.assertEquals("C", query1.object.resolve(None, None))

        query2 = select_node.query.queries[1]
        self.assertEquals(RDFQuery.QUERY, query2.query_type)
        self.assertIsInstance(query2.subject, TemplateNode)
        self.assertEquals(1, len(query2.subject.children))
        self.assertIsInstance(query2.subject.children[0], TemplateWordNode)
        self.assertEquals("?x", query2.subject.resolve(None, None))
        self.assertIsInstance(query2.predicate, TemplateNode)
        self.assertEquals("Y", query2.predicate.resolve(None, None))
        self.assertIsInstance(query2.object, TemplateNode)
        self.assertEquals("Z", query2.object.resolve(None, None))

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

        select_node = ast.children[0]
        self.assertIsNotNone(select_node.query)
        self.assertIsNotNone(select_node.query.vars)
        self.assertEquals(2, len(select_node.query.vars))
        self.assertTrue("?x" in select_node.query.vars)
        self.assertTrue("?y" in select_node.query.vars)

        self.assertEquals(2, len(select_node.query.queries))

        query1 = select_node.query.queries[0]
        self.assertEquals(RDFQuery.QUERY, query1.query_type)
        self.assertIsInstance(query1.subject, TemplateNode)
        self.assertEquals(1, len(query1.subject.children))
        self.assertIsInstance(query1.subject.children[0], TemplateWordNode)
        self.assertEquals("A", query1.subject.resolve(None, None))
        self.assertIsInstance(query1.predicate, TemplateNode)
        self.assertEquals("B", query1.predicate.resolve(None, None))
        self.assertIsInstance(query1.object, TemplateNode)
        self.assertEquals("C", query1.object.resolve(None, None))

        query2 = select_node.query.queries[1]
        self.assertEquals(RDFQuery.QUERY, query2.query_type)
        self.assertIsInstance(query2.subject, TemplateNode)
        self.assertEquals(1, len(query2.subject.children))
        self.assertIsInstance(query2.subject.children[0], TemplateWordNode)
        self.assertEquals("?x", query2.subject.resolve(None, None))
        self.assertIsInstance(query2.predicate, TemplateNode)
        self.assertEquals("?y", query2.predicate.resolve(None, None))
        self.assertIsInstance(query2.object, TemplateNode)
        self.assertEquals("Z", query2.object.resolve(None, None))

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
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateSelectNode)
        self.assertEqual(0, len(ast.children[0].children))

        select_node = ast.children[0]
        self.assertIsNotNone(select_node.query)
        self.assertIsNotNone(select_node.query.vars)
        self.assertEquals(1, len(select_node.query.vars))
        self.assertTrue("?x" in select_node.query.vars)

        self.assertEquals(2, len(select_node.query.queries))

        query1 = select_node.query.queries[0]
        self.assertEquals(RDFQuery.QUERY, query1.query_type)
        self.assertIsInstance(query1.subject, TemplateNode)
        self.assertEquals(1, len(query1.subject.children))
        self.assertIsInstance(query1.subject.children[0], TemplateWordNode)
        self.assertEquals("A", query1.subject.resolve(None, None))
        self.assertIsInstance(query1.predicate, TemplateNode)
        self.assertEquals("B", query1.predicate.resolve(None, None))
        self.assertIsInstance(query1.object, TemplateNode)
        self.assertEquals("C", query1.object.resolve(None, None))

        query2 = select_node.query.queries[1]
        self.assertEquals(RDFQuery.NOT_QUERY, query2.query_type)
        self.assertIsInstance(query2.subject, TemplateNode)
        self.assertEquals(1, len(query2.subject.children))
        self.assertIsInstance(query2.subject.children[0], TemplateWordNode)
        self.assertEquals("?x", query2.subject.resolve(None, None))
        self.assertIsInstance(query2.predicate, TemplateNode)
        self.assertEquals("?x", query2.predicate.resolve(None, None))
        self.assertIsInstance(query2.object, TemplateNode)
        self.assertEquals("Z", query2.object.resolve(None, None))

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
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateSelectNode)
        self.assertEqual(0, len(ast.children[0].children))

        select_node = ast.children[0]
        self.assertIsNotNone(select_node.query)
        self.assertIsNotNone(select_node.query.vars)
        self.assertEquals(2, len(select_node.query.vars))
        self.assertTrue("?A" in select_node.query.vars)
        self.assertTrue("?X" in select_node.query.vars)

        self.assertEquals(2, len(select_node.query.queries))

        query1 = select_node.query.queries[0]
        self.assertEquals(RDFQuery.QUERY, query1.query_type)
        self.assertIsInstance(query1.subject, TemplateNode)
        self.assertEquals(1, len(query1.subject.children))
        self.assertIsInstance(query1.subject.children[0], TemplateWordNode)
        self.assertEquals("?A", query1.subject.resolve(None, None))
        self.assertIsInstance(query1.predicate, TemplateNode)
        self.assertEquals("B", query1.predicate.resolve(None, None))
        self.assertIsInstance(query1.object, TemplateNode)
        self.assertEquals("C", query1.object.resolve(None, None))

        query2 = select_node.query.queries[1]
        self.assertEquals(RDFQuery.NOT_QUERY, query2.query_type)
        self.assertIsInstance(query2.subject, TemplateNode)
        self.assertEquals(1, len(query2.subject.children))
        self.assertIsInstance(query2.subject.children[0], TemplateWordNode)
        self.assertEquals("?X", query2.subject.resolve(None, None))
        self.assertIsInstance(query2.predicate, TemplateNode)
        self.assertEquals("Y", query2.predicate.resolve(None, None))
        self.assertIsInstance(query2.object, TemplateNode)
        self.assertEquals("Z", query2.object.resolve(None, None))

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
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateSelectNode)
        self.assertEqual(0, len(ast.children[0].children))

        select_node = ast.children[0]
        self.assertIsNotNone(select_node.query)
        self.assertIsNotNone(select_node.query.vars)
        self.assertEquals(0, len(select_node.query.vars))

        self.assertEquals(1, len(select_node.query.queries))

        query1 = select_node.query.queries[0]
        self.assertEquals(RDFQuery.QUERY, query1.query_type)
        self.assertIsInstance(query1.subject, TemplateNode)
        self.assertEquals(1, len(query1.subject.children))
        self.assertIsInstance(query1.subject.children[0], TemplateWordNode)
        self.assertEquals("A", query1.subject.resolve(None, None))
        self.assertIsInstance(query1.predicate, TemplateNode)
        self.assertEquals("B", query1.predicate.resolve(None, None))
        self.assertIsInstance(query1.object, TemplateNode)
        self.assertEquals("C", query1.object.resolve(None, None))

    def test_query_no_vars(self):
        self.test_bot.brain.rdf.add_entity("MONKEY", "legs", "2")
        self.test_bot.brain.rdf.add_entity("MONKEY", "hasFur", "true")
        self.test_bot.brain.rdf.add_entity("ZEBRA", "legs", "4")
        self.test_bot.brain.rdf.add_entity("BIRD", "legs", "2")
        self.test_bot.brain.rdf.add_entity("ELEPHANT", "trunk", "true")

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
        self.assertEquals('[["MONKEY", "legs", "2"]]', result)

    def test_not_query_no_vars(self):
        self.test_bot.brain.rdf.add_entity("MONKEY", "legs", "2")
        self.test_bot.brain.rdf.add_entity("MONKEY", "hasFur", "true")
        self.test_bot.brain.rdf.add_entity("ZEBRA", "legs", "4")
        self.test_bot.brain.rdf.add_entity("BIRD", "legs", "2")
        self.test_bot.brain.rdf.add_entity("ELEPHANT", "trunk", "true")

        template = ET.fromstring("""
                <template>
                    <select>
                        <notq><subj>MONKEY</subj><pred>legs</pred><obj>2</obj></notq>
                    </select>
                </template>
                """)

        ast = self.parser.parse_template_expression(template)

        result = ast.resolve(self.test_bot, self.test_clientid)
        self.assertIsNotNone(result)
        self.assertEquals('[["ZEBRA", "legs", "4"], ["BIRD", "legs", "2"], ["ELEPHANT", "trunk", "true"]]', result)

    def test_query_var(self):
        self.test_bot.brain.rdf.add_entity("MONKEY", "legs", "2")
        self.test_bot.brain.rdf.add_entity("MONKEY", "hasFur", "true")
        self.test_bot.brain.rdf.add_entity("ZEBRA", "legs", "4")
        self.test_bot.brain.rdf.add_entity("BIRD", "legs", "2")
        self.test_bot.brain.rdf.add_entity("ELEPHANT", "trunk", "true")

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
        self.assertEquals('[["?x", "MONKEY"], ["?x", "BIRD"]]', result)

    def test_not_query_var(self):
        self.test_bot.brain.rdf.add_entity("MONKEY", "legs", "2")
        self.test_bot.brain.rdf.add_entity("MONKEY", "hasFur", "true")
        self.test_bot.brain.rdf.add_entity("ZEBRA", "legs", "4")
        self.test_bot.brain.rdf.add_entity("BIRD", "legs", "2")
        self.test_bot.brain.rdf.add_entity("ELEPHANT", "trunk", "true")

        template = ET.fromstring("""
                <template>
                    <select>
                        <vars>?x</vars>
                        <notq><subj>?x</subj><pred>legs</pred><obj>2</obj></notq>
                    </select>
                </template>
                """)

        ast = self.parser.parse_template_expression(template)

        result = ast.resolve(self.test_bot, self.test_clientid)
        self.assertIsNotNone(result)
        self.assertEquals('[["?x", "ZEBRA"], ["?x", "ELEPHANT"]]', result)

    def test_query_multi_vars(self):
        self.test_bot.brain.rdf.add_entity("MONKEY", "legs", "2")
        self.test_bot.brain.rdf.add_entity("MONKEY", "hasFur", "true")
        self.test_bot.brain.rdf.add_entity("ZEBRA", "legs", "4")
        self.test_bot.brain.rdf.add_entity("BIRD", "legs", "2")
        self.test_bot.brain.rdf.add_entity("ELEPHANT", "trunk", "true")

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
        self.assertEquals('[["?x", "MONKEY"], ["?y", "legs"], ["?x", "BIRD"], ["?y", "legs"]]', result)

    def test_query_var_multi_queries(self):
        self.test_bot.brain.rdf.add_entity("MONKEY", "legs", "2")
        self.test_bot.brain.rdf.add_entity("MONKEY", "hasFur", "true")
        self.test_bot.brain.rdf.add_entity("ZEBRA", "legs", "4")
        self.test_bot.brain.rdf.add_entity("BIRD", "legs", "2")
        self.test_bot.brain.rdf.add_entity("ELEPHANT", "trunk", "true")

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
        self.assertEquals('[["?x", "MONKEY"]]', result)

    def test_query_var_mixed_queries(self):
        self.test_bot.brain.rdf.add_entity("MONKEY", "legs", "2")
        self.test_bot.brain.rdf.add_entity("MONKEY", "hasFur", "true")
        self.test_bot.brain.rdf.add_entity("ZEBRA", "legs", "4")
        self.test_bot.brain.rdf.add_entity("BIRD", "legs", "2")
        self.test_bot.brain.rdf.add_entity("ELEPHANT", "trunk", "true")

        template = ET.fromstring("""
                <template>
                    <select>
                        <vars>?x</vars>
                        <q><subj>?x</subj><pred>legs</pred><obj>2</obj></q>
                        <notq><subj>?x</subj><pred>hasFur</pred><obj>true</obj></notq>
                    </select>
                </template>
                """)

        ast = self.parser.parse_template_expression(template)

        result = ast.resolve(self.test_bot, self.test_clientid)
        self.assertIsNotNone(result)
        self.assertEquals('[["?x", "BIRD"]]', result)

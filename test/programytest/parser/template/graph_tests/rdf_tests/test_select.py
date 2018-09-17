import xml.etree.ElementTree as ET
import json

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.template.nodes.select import TemplateSelectNode
from programy.parser.template.nodes.select import Query, NotQuery
from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphSelectTests(TemplateGraphTestClient):

    ################################################################################################################
    # Test Node Construction
    #

    def test_select_single_vars_single_query(self):
        template = ET.fromstring("""
			<template>
			    <select>
			        <vars>?x</vars>
			        <q><subj>?x</subj><pred>Y</pred><obj>Z</obj></q>
			    </select>
			</template>
			""")

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateSelectNode)
        self.assertEqual(0, len(ast.children[0].children))

        select_node = ast.children[0]

        self.assertIsNotNone(select_node.vars)
        self.assertEqual(1, len(select_node.vars))
        self.assertTrue("?x" in select_node.vars)

        self.assertEqual(1, len(select_node.queries))
        query1 = select_node.queries[0]
        self.assertIsInstance(query1, Query)
        self.assertIsInstance(query1.subj, TemplateNode)
        self.assertEqual(1, len(query1.subj.children))
        self.assertIsInstance(query1.subj.children[0], TemplateWordNode)
        self.assertEqual("?x", query1.subj.resolve(self._client_context))
        self.assertIsInstance(query1.pred, TemplateNode)
        self.assertEqual("Y", query1.pred.resolve(self._client_context))
        self.assertIsInstance(query1.obj, TemplateNode)
        self.assertEqual("Z", query1.obj.resolve(self._client_context))

    def test_select_multi_vars_single_query(self):
        template = ET.fromstring("""
			<template>
			    <select>
			        <vars>?x ?y</vars>
			        <q><subj>?x</subj><pred>?y</pred><obj>Z</obj></q>
			    </select>
			</template>
			""")

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateSelectNode)
        self.assertEqual(0, len(ast.children[0].children))

        select_node = ast.children[0]

        self.assertIsNotNone(select_node.vars)
        self.assertEqual(2, len(select_node.vars))
        self.assertTrue("?x" in select_node.vars)
        self.assertTrue("?y" in select_node.vars)

        self.assertEqual(1, len(select_node.queries))
        query1 = select_node.queries[0]
        self.assertIsInstance(query1, Query)
        self.assertIsInstance(query1.subj, TemplateNode)
        self.assertEqual(1, len(query1.subj.children))
        self.assertIsInstance(query1.subj.children[0], TemplateWordNode)
        self.assertEqual("?x", query1.subj.resolve(self._client_context))
        self.assertIsInstance(query1.pred, TemplateNode)
        self.assertEqual("?y", query1.pred.resolve(self._client_context))
        self.assertIsInstance(query1.obj, TemplateNode)
        self.assertEqual("Z", query1.obj.resolve(self._client_context))

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

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateSelectNode)
        self.assertEqual(0, len(ast.children[0].children))

        select_node = ast.children[0]
        self.assertIsNotNone(select_node.vars)
        self.assertEqual(1, len(select_node.vars))
        self.assertTrue("?x" in select_node.vars)

        self.assertEqual(2, len(select_node.queries))

        query1 = select_node.queries[0]
        self.assertIsInstance(query1, Query)
        self.assertIsInstance(query1.subj, TemplateNode)
        self.assertEqual(1, len(query1.subj.children))
        self.assertIsInstance(query1.subj.children[0], TemplateWordNode)
        self.assertEqual("A", query1.subj.resolve(self._client_context))
        self.assertIsInstance(query1.pred, TemplateNode)
        self.assertEqual("B", query1.pred.resolve(self._client_context))
        self.assertIsInstance(query1.obj, TemplateNode)
        self.assertEqual("C", query1.obj.resolve(self._client_context))

        query2 = select_node.queries[1]
        self.assertIsInstance(query2, Query)
        self.assertIsInstance(query2.subj, TemplateNode)
        self.assertEqual(1, len(query2.subj.children))
        self.assertIsInstance(query2.subj.children[0], TemplateWordNode)
        self.assertEqual("?x", query2.subj.resolve(self._client_context))
        self.assertIsInstance(query2.pred, TemplateNode)
        self.assertEqual("Y", query2.pred.resolve(self._client_context))
        self.assertIsInstance(query2.obj, TemplateNode)
        self.assertEqual("Z", query2.obj.resolve(self._client_context))

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

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateSelectNode)
        self.assertEqual(0, len(ast.children[0].children))

        select_node = ast.children[0]
        self.assertIsNotNone(select_node.vars)
        self.assertEqual(2, len(select_node.vars))
        self.assertTrue("?x" in select_node.vars)
        self.assertTrue("?y" in select_node.vars)

        self.assertEqual(2, len(select_node.queries))

        query1 = select_node.queries[0]
        self.assertIsInstance(query1, Query)
        self.assertIsInstance(query1.subj, TemplateNode)
        self.assertEqual(1, len(query1.subj.children))
        self.assertIsInstance(query1.subj.children[0], TemplateWordNode)
        self.assertEqual("A", query1.subj.resolve(self._client_context))
        self.assertIsInstance(query1.pred, TemplateNode)
        self.assertEqual("B", query1.pred.resolve(self._client_context))
        self.assertIsInstance(query1.obj, TemplateNode)
        self.assertEqual("C", query1.obj.resolve(self._client_context))

        query2 = select_node.queries[1]
        self.assertIsInstance(query2, Query)
        self.assertIsInstance(query2.subj, TemplateNode)
        self.assertEqual(1, len(query2.subj.children))
        self.assertIsInstance(query2.subj.children[0], TemplateWordNode)
        self.assertEqual("?x", query2.subj.resolve(self._client_context))
        self.assertIsInstance(query2.pred, TemplateNode)
        self.assertEqual("?y", query2.pred.resolve(self._client_context))
        self.assertIsInstance(query2.obj, TemplateNode)
        self.assertEqual("Z", query2.obj.resolve(self._client_context))

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

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateSelectNode)
        self.assertEqual(0, len(ast.children[0].children))

        select_node = ast.children[0]
        self.assertIsNotNone(select_node.vars)
        self.assertEqual(1, len(select_node.vars))
        self.assertTrue("?x" in select_node.vars)

        self.assertEqual(2, len(select_node.queries))

        query1 = select_node.queries[0]
        self.assertIsInstance(query1, Query)
        self.assertIsInstance(query1.subj, TemplateNode)
        self.assertEqual(1, len(query1.subj.children))
        self.assertIsInstance(query1.subj.children[0], TemplateWordNode)
        self.assertEqual("A", query1.subj.resolve(self._client_context))
        self.assertIsInstance(query1.pred, TemplateNode)
        self.assertEqual("B", query1.pred.resolve(self._client_context))
        self.assertIsInstance(query1.obj, TemplateNode)
        self.assertEqual("C", query1.obj.resolve(self._client_context))

        query2 = select_node.queries[1]
        self.assertIsInstance(query2, NotQuery)
        self.assertIsInstance(query2.subj, TemplateNode)
        self.assertEqual(1, len(query2.subj.children))
        self.assertIsInstance(query2.subj.children[0], TemplateWordNode)
        self.assertEqual("?x", query2.subj.resolve(self._client_context))
        self.assertIsInstance(query2.pred, TemplateNode)
        self.assertEqual("?x", query2.pred.resolve(self._client_context))
        self.assertIsInstance(query2.obj, TemplateNode)
        self.assertEqual("Z", query2.obj.resolve(self._client_context))

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

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateSelectNode)
        self.assertEqual(0, len(ast.children[0].children))

        select_node = ast.children[0]
        self.assertIsNotNone(select_node)
        self.assertIsNotNone(select_node.vars)
        self.assertEqual(2, len(select_node.vars))
        self.assertTrue("?A" in select_node.vars)
        self.assertTrue("?X" in select_node.vars)

        self.assertEqual(2, len(select_node.queries))

        query1 = select_node.queries[0]
        self.assertIsInstance(query1, Query)
        self.assertIsInstance(query1.subj, TemplateNode)
        self.assertEqual(1, len(query1.subj.children))
        self.assertIsInstance(query1.subj.children[0], TemplateWordNode)
        self.assertEqual("?A", query1.subj.resolve(self._client_context))
        self.assertIsInstance(query1.pred, TemplateNode)
        self.assertEqual("B", query1.pred.resolve(self._client_context))
        self.assertIsInstance(query1.obj, TemplateNode)
        self.assertEqual("C", query1.obj.resolve(self._client_context))

        query2 = select_node.queries[1]
        self.assertIsInstance(query2, NotQuery)
        self.assertIsInstance(query2.subj, TemplateNode)
        self.assertEqual(1, len(query2.subj.children))
        self.assertIsInstance(query2.subj.children[0], TemplateWordNode)
        self.assertEqual("?X", query2.subj.resolve(self._client_context))
        self.assertIsInstance(query2.pred, TemplateNode)
        self.assertEqual("Y", query2.pred.resolve(self._client_context))
        self.assertIsInstance(query2.obj, TemplateNode)
        self.assertEqual("Z", query2.obj.resolve(self._client_context))

    def test_select_no_vars_single_query(self):
        template = ET.fromstring("""
                <template>
                    <select>
                        <q><subj>A</subj><pred>B</pred><obj>C</obj></q>
                    </select>
                </template>
                """)

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateSelectNode)
        self.assertEqual(0, len(ast.children[0].children))

        select_node = ast.children[0]
        self.assertIsNotNone(select_node)
        self.assertIsNotNone(select_node.vars)
        self.assertEqual(0, len(select_node.vars))

        self.assertEqual(1, len(select_node.queries))

        query1 = select_node.queries[0]
        self.assertIsInstance(query1, Query)
        self.assertIsInstance(query1.subj, TemplateNode)
        self.assertEqual(1, len(query1.subj.children))
        self.assertIsInstance(query1.subj.children[0], TemplateWordNode)
        self.assertEqual("A", query1.subj.resolve(self._client_context))
        self.assertIsInstance(query1.pred, TemplateNode)
        self.assertEqual("B", query1.pred.resolve(self._client_context))
        self.assertIsInstance(query1.obj, TemplateNode)
        self.assertEqual("C", query1.obj.resolve(self._client_context))

    ################################################################################################################
    # Test Matching Evaluation
    #

    def test_query_no_vars(self):
        self._client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("MONKEY", "HASFUR", "true", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ZEBRA", "LEGS", "4", "ANIMALS")
        self._client_context.brain.rdf.add_entity("BIRD", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ELEPHANT", "TRUNK", "true", "ANIMALS")

        template = ET.fromstring("""
                <template>
                    <select>
                        <q><subj>MONKEY</subj><pred>LEGS</pred><obj>2</obj></q>
                    </select>
                </template>
                """)

        ast = self._graph.parse_template_expression(template)

        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)

        query_results = json.loads(result)
        query1_results = query_results[0]
        query1_results_result1 = query1_results[0]

        self.assertTrue(["subj", "MONKEY"] in query1_results_result1)
        self.assertTrue(["pred", "LEGS"] in query1_results_result1)
        self.assertTrue(["obj", "2"] in query1_results_result1)

    def test_not_query_no_vars(self):
        self._client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("MONKEY", "HASFUR", "true", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ZEBRA", "LEGS", "4", "ANIMALS")
        self._client_context.brain.rdf.add_entity("BIRD", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ELEPHANT", "TRUNK", "true", "ANIMALS")

        template = ET.fromstring("""
                <template>
                    <select>
                        <notq><subj>MONKEY</subj><pred>LEGS</pred><obj>2</obj></notq>
                    </select>
                </template>
                """)

        ast = self._graph.parse_template_expression(template)

        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        query_results = json.loads(result)
        self.assertIsNotNone(query_results)

        self.assertTrue([['subj', 'ZEBRA'], ['pred', 'LEGS'], ['obj', '4']] in query_results[0])
        self.assertTrue([['subj', 'BIRD'], ['pred', 'LEGS'], ['obj', '2']] in query_results[0])
        self.assertTrue([['subj', 'ELEPHANT'], ['pred', 'TRUNK'], ['obj', 'true']] in query_results[0])

    def test_query_var(self):
        self._client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("MONKEY", "HASFUR", "true", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ZEBRA", "LEGS", "4", "ANIMALS")
        self._client_context.brain.rdf.add_entity("BIRD", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ELEPHANT", "TRUNK", "true", "ANIMALS")

        template = ET.fromstring("""
                <template>
                    <select>
                        <vars>?x</vars>
                        <q><subj>?x</subj><pred>LEGS</pred><obj>2</obj></q>
                    </select>
                </template>
                """)

        ast = self._graph.parse_template_expression(template)

        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        query_results = json.loads(result)
        self.assertIsNotNone(query_results)
        self.assertEqual(2, len(query_results))
        self.assertTrue([["?x", "MONKEY"]] in query_results)
        self.assertTrue([["?x", "BIRD"]] in query_results)

    def test_not_query_var(self):
        self._client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("MONKEY", "HASFUR", "true", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ZEBRA", "LEGS", "4", "ANIMALS")
        self._client_context.brain.rdf.add_entity("BIRD", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ELEPHANT", "TRUNK", "true", "ANIMALS")

        template = ET.fromstring("""
                <template>
                    <select>
                        <vars>?x</vars>
                        <notq><subj>?x</subj><pred>LEGS</pred><obj>2</obj></notq>
                    </select>
                </template>
                """)

        ast = self._graph.parse_template_expression(template)

        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        query_results = json.loads(result)
        self.assertIsNotNone(query_results)
        self.assertEqual(2, len(query_results))
        self.assertTrue([["?x", "ZEBRA"]] in query_results)
        self.assertTrue([["?x", "ELEPHANT"]] in query_results)

    def test_query_multi_vars(self):
        self._client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("MONKEY", "HASFUR", "true", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ZEBRA", "LEGS", "4", "ANIMALS")
        self._client_context.brain.rdf.add_entity("BIRD", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ELEPHANT", "TRUNK", "true", "ANIMALS")

        template = ET.fromstring("""
                <template>
                    <select>
                        <vars>?x ?y</vars>
                        <q><subj>?x</subj><pred>?y</pred><obj>2</obj></q>
                    </select>
                </template>
                """)

        ast = self._graph.parse_template_expression(template)

        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        query_results = json.loads(result)
        self.assertIsNotNone(query_results)
        self.assertEqual(2, len(query_results))
        self.assertTrue([["?x", "MONKEY"], ["?y", "LEGS"]] in query_results)
        self.assertTrue([["?x", "BIRD"], ["?y", "LEGS"]] in query_results)

    def test_query_var_multi_queries(self):
        self._client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("MONKEY", "HASFUR", "true", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ZEBRA", "LEGS", "4", "ANIMALS")
        self._client_context.brain.rdf.add_entity("BIRD", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ELEPHANT", "TRUNK", "true", "ANIMALS")

        template = ET.fromstring("""
                <template>
                    <select>
                        <vars>?x</vars>
                        <q><subj>?x</subj><pred>LEGS</pred><obj>2</obj></q>
                        <q><subj>?x</subj><pred>HASFUR</pred><obj>true</obj></q>
                    </select>
                </template>
                """)

        ast = self._graph.parse_template_expression(template)

        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        query_results = json.loads(result)
        self.assertIsNotNone(query_results)
        self.assertEqual(1, len(query_results))

        self.assertTrue([["?x", "MONKEY"]] in query_results)

    def test_query_var_mixed_queries(self):
        self._client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("MONKEY", "HASFUR", "true", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ZEBRA", "LEGS", "4", "ANIMALS")
        self._client_context.brain.rdf.add_entity("BIRD", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ELEPHANT", "TRUNK", "true", "ANIMALS")

        template = ET.fromstring("""
                <template>
                    <select>
                        <vars>?x</vars>
                        <q><subj>?x</subj><pred>LEGS</pred><obj>2</obj></q>
                        <notq><subj>?x</subj><pred>HASFUR</pred><obj>true</obj></notq>
                    </select>
                </template>
                """)

        ast = self._graph.parse_template_expression(template)

        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        query_results = json.loads(result)
        self.assertIsNotNone(query_results)
        self.assertEqual(1, len(query_results))

        self.assertTrue([["?x", "BIRD"]] in query_results)

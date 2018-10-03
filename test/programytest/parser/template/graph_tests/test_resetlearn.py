import xml.etree.ElementTree as ET

from programy.parser.template.nodes.resetlearn import TemplateResetLearnNode
from programy.parser.exceptions import ParserException
from programy.parser.template.nodes.base import TemplateNode
from programy.context import ClientContext
from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration

from programytest.client import TestClient
from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient

class TemplateGraphResetLearnTests(TemplateGraphTestClient):

     def test_learnf_type1(self):
        template = ET.fromstring("""
			<template>
				<resetlearn />
			</template>
			""")

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateResetLearnNode)
        self.assertEqual(0, len(ast.children[0].children))

     def test_learnf_type2(self):
        template = ET.fromstring("""
			<template>
				<resetlearn></resetlearn>
			</template>
			""")

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateResetLearnNode)
        self.assertEqual(0, len(ast.children[0].children))

     def test_request_with_children(self):
        template = ET.fromstring("""
			<template>
				<resetlearn>Error</resetlearn>
			</template>
			""")
        with self.assertRaises(ParserException):
            ast = self._graph.parse_template_expression(template)

     def test_removal(self):
        client_context1 = self.create_client_context("testid")

        template = ET.fromstring("""
        			<template>
        				<learn>
        				    <category>
        				        <pattern>HELLO THERE</pattern>
        				        <template>HIYA ONE</template>
        				    </category>
        				</learn>
        			</template>
        			""")

        ast = self._graph.parse_template_expression(template)

        learn_node = ast.children[0]

        learn_node.resolve(client_context1)

        response = client_context1.bot.ask_question(client_context1, "HELLO THERE")
        self.assertEqual("HIYA ONE.", response)

        client_context2 = self.create_client_context("testid")

        template = ET.fromstring("""
        			<template>
        				<learn>
        				    <category>
        				        <pattern>HELLO THERE</pattern>
        				        <template>HIYA TWO</template>
        				    </category>
        				</learn>
        			</template>
        			""")

        ast = self._graph.parse_template_expression(template)

        learn_node = ast.children[0]

        learn_node.resolve(client_context2)

        response = client_context2.bot.ask_question(client_context2, "HELLO THERE")
        self.assertEqual("HIYA TWO.", response)

        template = ET.fromstring("""
        			<template>
        				<resetlearn />
        			</template>
        			""")

        ast = self._graph.parse_template_expression(template)

        learn_node = ast.children[0]

        learn_node.resolve(client_context2)


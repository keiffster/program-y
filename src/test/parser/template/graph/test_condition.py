import unittest
import xml.etree.ElementTree as ET

from programy.bot import Bot
from programy.brain import Brain
from programy.config import ClientConfiguration, BrainConfiguration
from programy.dialog import Question, Sentence
from programy.parser.template.graph import TemplateGraph
from programy.parser.template.nodes import *


class TemplateGraphConditionTests(unittest.TestCase):

    def setUp(self):
        self.parser = TemplateGraph()
        self.assertIsNotNone(self.parser)

        self.test_brain = None
        self.test_sentence = Sentence("test sentence")
        self.test_sentence._stars = ['one', 'two', 'three', 'four', 'five', 'six']
        self.test_sentence._thatstars = ["*"]
        self.test_sentence._topicstars = ["*"]

        test_config = ClientConfiguration()

        self.test_bot = Bot(Brain(BrainConfiguration()), config=test_config.bot_configuration)
        self.test_clientid = "testid"

        conversation = self.test_bot.get_conversation(self.test_clientid)
        question = Question.create_from_sentence(self.test_sentence)
        conversation._questions.append(question)

    def test_condition_template_no_attribs(self):
        template = ET.fromstring("""
			<template>
				<condition>
				</condition>
			</template>
			""")
        with self.assertRaises(ParserException):
            self.parser.parse_template_expression(template)

    def test_condition_template_type1_variant1_name(self):
        template = ET.fromstring("""
			<template>
				<condition name="aname" value="avalue">X <random><li>1</li><li>2</li></random> Y</condition>
			</template>
			""")
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateType1ConditionNode)

        self.assertFalse(template_node.local)
        self.assertEqual(template_node.name, "aname")
        self.assertEqual(template_node.value, "avalue")

        self.assertEqual(len(template_node.children), 3)

    def test_condition_template_type1_variant1_var(self):
        template = ET.fromstring("""
            <template>
                <condition var="aname" value="avalue">X <random><li>1</li><li>2</li></random> Y</condition>
            </template>
            """)
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateType1ConditionNode)

        self.assertTrue(template_node.local)
        self.assertEqual(template_node.name, "aname")
        self.assertEqual(template_node.value, "avalue")

        self.assertEqual(len(template_node.children), 3)

    def test_condition_template_type1_variant2_name(self):
        template = ET.fromstring("""
			<template>
				<condition name="aname"><value>avalue</value>X</condition>
			</template>
			""")
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateType1ConditionNode)

        self.assertFalse(template_node.local)
        self.assertEqual(template_node.name, "aname")
        self.assertEqual(template_node.value, "avalue")

        self.assertEqual(len(template_node.children), 1)

    def test_condition_template_type1_variant2_var(self):
        template = ET.fromstring("""
            <template>
                <condition var="aname"><value>avalue</value>X</condition>
            </template>
            """)
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateType1ConditionNode)

        self.assertTrue(template_node.local)
        self.assertEqual(template_node.name, "aname")
        self.assertEqual(template_node.value, "avalue")

        self.assertEqual(len(template_node.children), 1)

    def test_condition_template_type1_variant3_name(self):
        template = ET.fromstring("""
			<template>
				<condition value="avalue"><name>aname</name>X</condition>
			</template>
			""")
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateType1ConditionNode)
        self.assertFalse(template_node.local)
        self.assertEqual(template_node.name, "aname")
        self.assertEqual(template_node.value, "avalue")

        self.assertEqual(len(template_node.children), 1)

    def test_condition_template_type1_variant3_var(self):
        template = ET.fromstring("""
            <template>
                <condition value="avalue"><var>aname</var>X</condition>
            </template>
            """)
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateType1ConditionNode)

        self.assertTrue(template_node.local)
        self.assertEqual(template_node.name, "aname")
        self.assertEqual(template_node.value, "avalue")

        self.assertEqual(len(template_node.children), 1)

    def test_condition_template_type1_variant4_name(self):
        template = ET.fromstring("""
			<template>
				<condition><name>aname</name><value>avalue</value>X</condition>
			</template>
			""")
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateType1ConditionNode)

        self.assertFalse(template_node.local)
        self.assertEqual(template_node.name, "aname")
        self.assertEqual(template_node.value, "avalue")

        self.assertEqual(len(template_node.children), 1)

    def test_condition_template_type1_variant4_var(self):
        template = ET.fromstring("""
            <template>
                <condition><var>aname</var><value>avalue</value>X</condition>
            </template>
            """)
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateType1ConditionNode)

        self.assertTrue(template_node.local)
        self.assertEqual(template_node.name, "aname")
        self.assertEqual(template_node.value, "avalue")

        self.assertEqual(len(template_node.children), 1)

    def test_condition_template_type2_variant1_name(self):
        template = ET.fromstring("""
			<template>
				<condition>
					<name>aname</name>
					<li value="a">A</li>
					<li value="b">B</li>
					<li><value>c</value>C</li>
					<li>D</li>
				</condition>
			</template>
			""")
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateType2ConditionNode)
        self.assertFalse(template_node.local)
        self.assertEqual(template_node.name, "aname")
        self.assertEqual(len(template_node.children), 4)

        node = template_node.children[0]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertFalse(node.local)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertEqual(node.value, "a")
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(None, None), "A")

        node = template_node.children[1]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertFalse(node.local)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertEqual(node.value, "b")
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(None, None), "B")

        node = template_node.children[2]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertFalse(node.local)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertEqual(node.value, "c")
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(None, None), "C")

        node = template_node.children[3]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertFalse(node.local)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsNone(node.value)
        self.assertTrue(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(None, None), "D")

    def test_condition_template_type2_variant1_name_with_loop(self):
        template = ET.fromstring("""
            <template>
                <condition>
                    <name>aname</name>
                    <li value="a">A <loop /></li>
                    <li value="b">B</li>
                    <li><value>c</value>C</li>
                    <li>D</li>
                </condition>
            </template>
            """)
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateType2ConditionNode)
        self.assertFalse(template_node.local)
        self.assertEqual(template_node.name, "aname")
        self.assertEqual(len(template_node.children), 4)

        node = template_node.children[0]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertFalse(node.local)
        self.assertTrue(node.loop)
        self.assertIsNone(node.name)
        self.assertEqual(node.value, "a")
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(None, None), "A")

        node = template_node.children[1]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertFalse(node.local)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertEqual(node.value, "b")
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(None, None), "B")

        node = template_node.children[2]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertFalse(node.local)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertEqual(node.value, "c")
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(None, None), "C")

        node = template_node.children[3]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertFalse(node.local)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsNone(node.value)
        self.assertTrue(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(None, None), "D")

    def test_condition_template_type2_variant1_var(self):
        template = ET.fromstring("""
            <template>
                <condition>
                    <var>aname</var>
                    <li value="a">A</li>
                    <li value="b">B</li>
                    <li><value>c</value>C</li>
                    <li>D</li>
                </condition>
            </template>
            """)
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateType2ConditionNode)
        self.assertTrue(template_node.local)
        self.assertEqual(template_node.name, "aname")
        self.assertEqual(len(template_node.children), 4)

        node = template_node.children[0]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertTrue(node.local)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertEqual(node.value, "a")
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(None, None), "A")

        node = template_node.children[1]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertTrue(node.local)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertEqual(node.value, "b")
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(None, None), "B")

        node = template_node.children[2]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertTrue(node.local)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertEqual(node.value, "c")
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(None, None), "C")

        node = template_node.children[3]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertTrue(node.local)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsNone(node.value)
        self.assertTrue(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(None, None), "D")

    def test_condition_template_type2_variant2_name(self):
        template = ET.fromstring("""
			<template>
				<condition name="aname">
					<li value="a">A</li>
					<li value="b">B</li>
					<li><value>c</value>C</li>
					<li>D</li>
				</condition>
			</template>
			""")
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateType2ConditionNode)
        self.assertFalse(template_node.local)
        self.assertEqual(template_node.name, "aname")
        self.assertEqual(len(template_node.children), 4)

        node = template_node.children[0]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertFalse(node.local)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertEqual(node.value, "a")
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(None, None), "A")

        node = template_node.children[1]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertFalse(node.local)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertEqual(node.value, "b")
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(None, None), "B")

        node = template_node.children[2]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertFalse(node.local)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertEqual(node.value, "c")
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(None, None), "C")

        node = template_node.children[3]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertFalse(node.local)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsNone(node.value)
        self.assertTrue(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(None, None), "D")

    def test_condition_template_type2_variant2_var(self):
        template = ET.fromstring("""
            <template>
                <condition var="aname">
                    <li value="a">A</li>
                    <li value="b">B</li>
                    <li><value>c</value>C</li>
                    <li>D</li>
                </condition>
            </template>
            """)
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateType2ConditionNode)
        self.assertTrue(template_node.local)
        self.assertEqual(template_node.name, "aname")
        self.assertEqual(len(template_node.children), 4)

        node = template_node.children[0]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertTrue(node.local)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertEqual(node.value, "a")
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(None, None), "A")

        node = template_node.children[1]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertTrue(node.local)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertEqual(node.value, "b")
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(None, None), "B")

        node = template_node.children[2]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertTrue(node.local)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertEqual(node.value, "c")
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(None, None), "C")

        node = template_node.children[3]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertTrue(node.local)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsNone(node.value)
        self.assertTrue(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(None, None), "D")

    def test_condition_template_type3_variant1_name(self):
        template = ET.fromstring("""
			<template>
				<condition>
					<li name='name1' value="a">Val1</li>
					<li value="b"><name>name2</name>Val2</li>
					<li name="name3"><value>c</value>Val3</li>
					<li><name>name4</name><value>d</value>Val4</li>
					<li>Val5</li>
				</condition>
			</template>
			""")
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]

        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateType3ConditionNode)
        self.assertEqual(len(template_node.children), 5)

        node = template_node.children[0]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertFalse(node.local)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name, "name1")
        self.assertIsNotNone(node.value)
        self.assertEqual(node.value, "a")
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(None, None), "Val1")

        node = template_node.children[1]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertFalse(node.local)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name, "name2")
        self.assertIsNotNone(node.value)
        self.assertEqual(node.value, "b")
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(None, None), "Val2")

        node = template_node.children[2]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertFalse(node.local)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name, "name3")
        self.assertIsNotNone(node.value)
        self.assertEqual(node.value, "c")
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(None, None), "Val3")

        node = template_node.children[3]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertFalse(node.local)
        self.assertFalse(node.loop)
        self.assertEqual(node.name, "name4")
        self.assertIsNotNone(node.value)
        self.assertEqual(node.value, "d")
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(None, None), "Val4")

        node = template_node.children[4]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertFalse(node.local)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsNone(node.value)
        self.assertTrue(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(None, None), "Val5")

    def test_condition_template_type3_variant1_name_with_loop(self):
        template = ET.fromstring("""
            <template>
                <condition>
                    <li name='name1' value="a">Val1 <loop /></li>
                    <li value="b"><name>name2</name>Val2</li>
                    <li name="name3"><value>c</value>Val3</li>
                    <li><name>name4</name><value>d</value>Val4</li>
                    <li>Val5</li>
                </condition>
            </template>
            """)
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]

        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateType3ConditionNode)
        self.assertEqual(len(template_node.children), 5)

        node = template_node.children[0]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertFalse(node.local)
        self.assertTrue(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name, "name1")
        self.assertIsNotNone(node.value)
        self.assertEqual(node.value, "a")
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(None, None), "Val1")

        node = template_node.children[1]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertFalse(node.local)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name, "name2")
        self.assertIsNotNone(node.value)
        self.assertEqual(node.value, "b")
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(None, None), "Val2")

        node = template_node.children[2]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertFalse(node.local)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name, "name3")
        self.assertIsNotNone(node.value)
        self.assertEqual(node.value, "c")
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(None, None), "Val3")

        node = template_node.children[3]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertFalse(node.local)
        self.assertFalse(node.loop)
        self.assertEqual(node.name, "name4")
        self.assertIsNotNone(node.value)
        self.assertEqual(node.value, "d")
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(None, None), "Val4")

        node = template_node.children[4]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertFalse(node.local)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsNone(node.value)
        self.assertTrue(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(None, None), "Val5")

    def test_condition_template_type3_variant1_var(self):
        template = ET.fromstring("""
			<template>
				<condition>
					<li var='name1' value="a">Val1</li>
					<li value="b"><var>name2</var>Val2</li>
					<li var="name3"><value>c</value>Val3</li>
					<li><var>name4</var><value>d</value>Val4</li>
					<li>Val5</li>
				</condition>
			</template>
			""")
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)

        template_node = ast.children[0]

        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, TemplateType3ConditionNode)
        self.assertEqual(len(template_node.children), 5)

        node = template_node.children[0]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertTrue(node.local)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name, "name1")
        self.assertIsNotNone(node.value)
        self.assertEqual(node.value, "a")
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(None, None), "Val1")

        node = template_node.children[1]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertTrue(node.local)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name, "name2")
        self.assertIsNotNone(node.value)
        self.assertEqual(node.value, "b")
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(None, None), "Val2")

        node = template_node.children[2]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertTrue(node.local)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name, "name3")
        self.assertIsNotNone(node.value)
        self.assertEqual(node.value, "c")
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(None, None), "Val3")

        node = template_node.children[3]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertTrue(node.local)
        self.assertFalse(node.loop)
        self.assertIsNotNone(node.name)
        self.assertEqual(node.name, "name4")
        self.assertIsNotNone(node.value)
        self.assertEqual(node.value, "d")
        self.assertFalse(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(None, None), "Val4")

        node = template_node.children[4]
        self.assertIsInstance(node, TemplateConditionListItemNode)
        self.assertFalse(node.local)
        self.assertFalse(node.loop)
        self.assertIsNone(node.name)
        self.assertIsNone(node.value)
        self.assertTrue(node.is_default())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].resolve(None, None), "Val5")

if __name__ == '__main__':
    unittest.main()

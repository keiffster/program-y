from unittest.mock import patch
import xml.etree.ElementTree as ET
from programy.dialog.question import Question
from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.condition import TemplateConditionListItemNode
from programy.parser.template.nodes.condition import TemplateConditionNode
from programy.parser.template.nodes.word import TemplateWordNode
from programytest.parser.base import ParserTestsBaseClass


class TemplateConditionType2NodeTests(ParserTestsBaseClass):

    def test_type2_node_global(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateConditionNode("cond1", condition_type=2)
        self.assertIsNotNone(node)
        cond1 = TemplateConditionListItemNode(value=TemplateWordNode("value1"))
        cond1.append(TemplateWordNode("Word1"))
        node.append(cond1)
        cond2 = TemplateConditionListItemNode(value=TemplateWordNode("value2"))
        cond2.append(TemplateWordNode("Word2"))
        node.append(cond2)
        cond3 = TemplateConditionListItemNode()
        cond3.append(TemplateWordNode("Word3"))
        node.append(cond3)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.bot.get_conversation(self._client_context).set_property('cond1', "value2")

        question = Question.create_from_text(self._client_context, "Hello")
        self._client_context.bot.get_conversation(self._client_context).record_dialog(question)
        self._client_context.bot.get_conversation(self._client_context).current_question().set_property("cond1", "value2")

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("Word2", result)

    def patch_resolve_type2_to_string(self, client_context):
        raise Exception ("Mock Exception")

    @patch("programy.parser.template.nodes.condition.TemplateConditionNode._resolve_type2_to_string", patch_resolve_type2_to_string)
    def test_type2_exception(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateConditionNode("cond1", condition_type=2)
        self.assertIsNotNone(node)
        cond1 = TemplateConditionListItemNode(value=TemplateWordNode("value1"))
        cond1.append(TemplateWordNode("Word1"))
        node.append(cond1)
        cond2 = TemplateConditionListItemNode(value=TemplateWordNode("value2"))
        cond2.append(TemplateWordNode("Word2"))
        node.append(cond2)
        cond3 = TemplateConditionListItemNode()
        cond3.append(TemplateWordNode("Word3"))
        node.append(cond3)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.bot.get_conversation(self._client_context).set_property('cond1', "value2")

        question = Question.create_from_text(self._client_context, "Hello")
        self._client_context.bot.get_conversation(self._client_context).record_dialog(question)
        self._client_context.bot.get_conversation(self._client_context).current_question().set_property("cond1", "value2")

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

    def test_type2_to_xml_global(self):
        root = TemplateNode()

        node = TemplateConditionNode("cond1", condition_type=2)
        self.assertIsNotNone(node)
        cond1 = TemplateConditionListItemNode(value=TemplateWordNode("value1"))
        cond1.append(TemplateWordNode("Word1"))
        node.append(cond1)
        cond2 = TemplateConditionListItemNode(value=TemplateWordNode("value2"))
        cond2.append(TemplateWordNode("Word2"))
        node.append(cond2)
        cond3 = TemplateConditionListItemNode()
        cond3.append(TemplateWordNode("Word3"))
        node.append(cond3)

        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><condition name="cond1"><li><value>value1</value>Word1</li> <li><value>value2</value>Word2</li> <li>Word3</li></condition></template>', xml_str)

    ###################################################################################################################
    # Type 2 Local
    #

    def test_type2_node_local(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateConditionNode("var1", var_type=TemplateConditionNode.LOCAL, condition_type=2)
        self.assertIsNotNone(node)
        cond1 = TemplateConditionListItemNode(value=TemplateWordNode("value1"), var_type=TemplateConditionNode.LOCAL)
        cond1.append(TemplateWordNode("Word1"))
        node.append(cond1)
        cond2 = TemplateConditionListItemNode(value=TemplateWordNode("value2"), var_type=TemplateConditionNode.LOCAL)
        cond2.append(TemplateWordNode("Word2"))
        node.append(cond2)
        cond3 = TemplateConditionListItemNode()
        cond3.append(TemplateWordNode("Word3"))
        node.append(cond3)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        question = Question.create_from_text(self._client_context, "Hello")
        self._client_context.bot.get_conversation(self._client_context).record_dialog(question)
        self._client_context.bot.get_conversation(self._client_context).current_question().set_property("var1", "value2")

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("Word2", result)

    def test_type2_to_xml_local(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateConditionNode("var1", var_type=TemplateConditionNode.LOCAL, condition_type=2)
        self.assertIsNotNone(node)
        cond1 = TemplateConditionListItemNode(value=TemplateWordNode("value1"), var_type=TemplateConditionNode.LOCAL)
        cond1.append(TemplateWordNode("Word1"))
        node.append(cond1)
        cond2 = TemplateConditionListItemNode(value=TemplateWordNode("value2"), var_type=TemplateConditionNode.LOCAL)
        cond2.append(TemplateWordNode("Word2"))
        node.append(cond2)
        cond3 = TemplateConditionListItemNode()
        cond3.append(TemplateWordNode("Word3"))
        node.append(cond3)

        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><condition var="var1"><li><value>value1</value>Word1</li> <li><value>value2</value>Word2</li> <li>Word3</li></condition></template>', xml_str)

    ###################################################################################################################
    # Type 2 Bot
    #

    def test_type2_node_bot(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateConditionNode("cond1", var_type=TemplateConditionNode.BOT, condition_type=2)
        self.assertIsNotNone(node)
        cond1 = TemplateConditionListItemNode(value=TemplateWordNode("value1"), var_type=TemplateConditionNode.BOT)
        cond1.append(TemplateWordNode("Word1"))
        node.append(cond1)
        cond2 = TemplateConditionListItemNode(value=TemplateWordNode("value2"), var_type=TemplateConditionNode.BOT)
        cond2.append(TemplateWordNode("Word2"))
        node.append(cond2)
        cond3 = TemplateConditionListItemNode()
        cond3.append(TemplateWordNode("Word3"))
        node.append(cond3)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.brain.properties.add_property('cond1', "value2")

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("Word2", result)

    def test_type2_to_xml_bot(self):
        root = TemplateNode()

        node = TemplateConditionNode("cond1", var_type=TemplateConditionNode.BOT, condition_type=2)
        self.assertIsNotNone(node)
        cond1 = TemplateConditionListItemNode(value=TemplateWordNode("value1"))
        cond1.append(TemplateWordNode("Word1"))
        node.append(cond1)
        cond2 = TemplateConditionListItemNode(value=TemplateWordNode("value2"))
        cond2.append(TemplateWordNode("Word2"))
        node.append(cond2)
        cond3 = TemplateConditionListItemNode()
        cond3.append(TemplateWordNode("Word3"))
        node.append(cond3)

        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><condition bot="cond1"><li><value>value1</value>Word1</li> <li><value>value2</value>Word2</li> <li>Word3</li></condition></template>', xml_str)

    def test_resolve_type2_condition(self):
        template = ET.fromstring("""
        			<template>
        				<condition>
        					<li name='name1' value="a">Val1</li>
        					<li>Val5</li>
        				</condition>
        			</template>
        			""")
        graph = self._client_context.bot.brain.aiml_parser.template_parser
        ast = graph.parse_template_expression(template)

        template_node = ast.children[0]
        self.assertEquals("Val5", template_node.resolve_type2_condition(self._client_context))

    def test_resolve_type2_condition_no_default(self):
        template = ET.fromstring("""
        			<template>
        				<condition>
        					<li name='name1' value="a">Val1</li>
        				</condition>
        			</template>
        			""")
        graph = self._client_context.bot.brain.aiml_parser.template_parser
        ast = graph.parse_template_expression(template)

        template_node = ast.children[0]
        self.assertEquals("", template_node.resolve_type2_condition(self._client_context))

import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.template.nodes.condlistitem import TemplateConditionListItemNode
from programy.parser.template.nodes.condtype2 import TemplateType2ConditionNode
from programy.dialog import Question

from test.parser.template.base import TemplateTestsBaseClass


class TemplateType2ConditionNodeTests(TemplateTestsBaseClass):

    def test_node_global(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateType2ConditionNode("cond1")
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

        self.bot.conversation(self.clientid)._predicates['cond1'] = "value2"

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual("Word2", result)

    def test_node_local(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateType2ConditionNode("var1", local=True)
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

        question = Question.create_from_text("Hello")
        self.bot.conversation(self.clientid).record_dialog(question)
        self.bot.conversation(self.clientid).current_question().set_predicate("var1", "value2")

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual("Word2", result)

    # TODO Add unit tests for <loop /> construct

    def test_to_xml_global(self):
        root = TemplateNode()

        node = TemplateType2ConditionNode("cond1")
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

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><condition name="cond1"><li><value>value1</value>Word1</li><li><value>value2</value>Word2</li><li>Word3</li></condition></template>', xml_str)

    def test_to_xml_local(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateType2ConditionNode("var1", local=True)
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

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><condition var="var1"><li><value>value1</value>Word1</li><li><value>value2</value>Word2</li><li>Word3</li></condition></template>', xml_str)

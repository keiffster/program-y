import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.template.nodes.condtype1 import TemplateType1ConditionNode
from programy.dialog import Question

from test.parser.template.base import TemplateTestsBaseClass


class TemplateType1ConditionNodeTests(TemplateTestsBaseClass):

    def test_node_global_match(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateType1ConditionNode("name1", TemplateWordNode("value1"), local=False)
        self.assertIsNotNone(node)

        node.append(TemplateWordNode("Hello"))
        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.bot.conversation(self.clientid)._predicates['name1'] = "value1"

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual(result, "Hello")

    def test_node_global_nomatch(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateType1ConditionNode("name1", TemplateWordNode("value1"), local=False)
        self.assertIsNotNone(node)

        node.append(TemplateWordNode("Hello"))
        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.bot.conversation(self.clientid)._predicates['name1'] = "value2"

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual(result, "")

    def test_node_local_match(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateType1ConditionNode("var1", TemplateWordNode("value1"), local=True)
        self.assertIsNotNone(node)

        node.append(TemplateWordNode("Hello"))
        root.append(node)
        self.assertEqual(len(root.children), 1)

        question = Question.create_from_text("Hello")
        self.bot.conversation(self.clientid).record_dialog(question)
        self.bot.conversation(self.clientid).current_question().set_predicate("var1", "value1")

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual(result, "Hello")

    def test_node_local_nomatch(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateType1ConditionNode("var1", TemplateWordNode("value1"), local=True)
        self.assertIsNotNone(node)

        node.append(TemplateWordNode("Hello"))
        root.append(node)
        self.assertEqual(len(root.children), 1)

        question = Question.create_from_text("Hello")
        self.bot.conversation(self.clientid).record_dialog(question)
        self.bot.conversation(self.clientid).current_question().set_predicate("var1", "value2")

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual(result, "")

    def test_to_xml_global(self):
        root = TemplateNode()
        node = TemplateType1ConditionNode("name1", TemplateWordNode("value1"), local=False)
        node.append(TemplateWordNode("Hello"))
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><condition name="name1"><value>value1</value>Hello</condition></template>', xml_str)

    def test_to_xml_local(self):
        root = TemplateNode()
        node = TemplateType1ConditionNode("name1", TemplateWordNode("value1"), local=True)
        node.append(TemplateWordNode("Hello"))
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><condition var="name1"><value>value1</value>Hello</condition></template>', xml_str)


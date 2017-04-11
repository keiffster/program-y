import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.get import TemplateGetNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.dialog import Question

from test.parser.template.base import TemplateTestsBaseClass


class TemplateGetNodeTests(TemplateTestsBaseClass):

    def test_local_get(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateGetNode()
        node.name = TemplateWordNode("name")
        node.local = True
        node.append(TemplateWordNode("Fred"))
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = self.bot.get_conversation(self.clientid)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text("Hello")
        conversation.record_dialog(question)
        self.assertIsNotNone(conversation.current_question())
        question.set_predicate("name", "keith")

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual("keith", result)

    def test_to_xml_local_get(self):
        root = TemplateNode()
        node = TemplateGetNode()
        node.name = TemplateWordNode("name")
        node.local = True
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><get var="name" /></template>', xml_str)

    def test_local_no_value(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateGetNode()
        node.name = TemplateWordNode("name")
        node.local = True
        node.append(TemplateWordNode("Fred"))
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.bot.brain.properties.add_property("default-get", "unknown")

        conversation = self.bot.get_conversation(self.clientid)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text("Hello")
        conversation.record_dialog(question)

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)

    def test_global_get(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateGetNode()
        node.name = TemplateWordNode("name")
        node.local = False
        node.append(TemplateWordNode("Fred"))
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = self.bot.get_conversation(self.clientid)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text("Hello")
        conversation.record_dialog(question)
        self.assertIsNotNone(conversation.current_question())
        conversation.set_predicate("name", "keith")

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual("keith", result)

    def test_to_xml_global_get(self):
        root = TemplateNode()
        node = TemplateGetNode()
        node.name = TemplateWordNode("name")
        node.local = False
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><get name="name" /></template>', xml_str)

    def test_global_get_no_value(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateGetNode()
        node.name = TemplateWordNode("name")
        node.local = False
        node.append(TemplateWordNode("Fred"))
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.bot.brain.properties.add_property("default-get", "unknown")

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)


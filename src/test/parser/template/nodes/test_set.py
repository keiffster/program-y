import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.set import TemplateSetNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.dialog import Question

from test.parser.template.base import TemplateTestsBaseClass


class TemplateSetNodeTests(TemplateTestsBaseClass):

    def test_local_set(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateSetNode()
        self.assertIsNotNone(node)
        node.name = TemplateWordNode("name")
        node.local = True
        node.append(TemplateWordNode("keith"))

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = self.bot.get_conversation(self.clientid)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text("Hello")
        conversation.record_dialog(question)
        self.assertIsNotNone(conversation.current_question())

        result = node.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual("keith", result)

        self.assertEqual("keith", question.predicate("name"))

    def test_to_xml_local_set(self):
        root = TemplateNode()
        node = TemplateSetNode()
        node.name = TemplateWordNode("name")
        node.local = True
        root.append(node)
        node.append(TemplateWordNode("keith"))

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><set var="name">keith</set></template>', xml_str)

    def test_global_set_allow_overrides_no_default(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        self.bot._configuration.override_predicates = True

        node = TemplateSetNode()
        self.assertIsNotNone(node)
        node.name = TemplateWordNode("name")
        node.local = False
        node.append(TemplateWordNode("keith"))

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = self.bot.get_conversation(self.clientid)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text("Hello")
        conversation.record_dialog(question)
        self.assertIsNotNone(conversation.current_question())

        result = node.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual("keith", result)

        self.assertEqual("keith", conversation.predicate("name"))

    def test_global_set_allow_overrides_with_default(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        self.bot._configuration.override_predicates = True
        self.bot.brain.properties.pairs.append(["name", "fred"])

        node = TemplateSetNode()
        self.assertIsNotNone(node)
        node.name = TemplateWordNode("name")
        node.local = False
        node.append(TemplateWordNode("keith"))

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = self.bot.get_conversation(self.clientid)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text("Hello")
        conversation.record_dialog(question)
        self.assertIsNotNone(conversation.current_question())

        result = node.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual("keith", result)

        self.assertEqual("keith", conversation.predicate("name"))

    def test_global_set_deny_overrides_with_default(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        self.bot._configuration.override_predicates = False
        self.bot.brain.properties.pairs.append(["name", "fred"])

        node = TemplateSetNode()
        self.assertIsNotNone(node)
        node.name = TemplateWordNode("name")
        node.local = False
        node.append(TemplateWordNode("keith"))

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = self.bot.get_conversation(self.clientid)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text("Hello")
        conversation.record_dialog(question)
        self.assertIsNotNone(conversation.current_question())

        result = node.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual("fred", result)

        self.assertEqual(None, conversation.predicate("name"))

    def test_to_xml_global_set(self):
        root = TemplateNode()
        node = TemplateSetNode()
        node.name = TemplateWordNode("name")
        node.local = False
        root.append(node)
        node.append(TemplateWordNode("keith"))

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><set name="name">keith</set></template>', xml_str)


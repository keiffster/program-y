import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.that import TemplateThatNode
from programy.dialog import Conversation, Question

from test.parser.template.base import TemplateTestsBaseClass


class TemplateThatNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateThatNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        # Text that with no bot and therefore no conversation, "" is returned
        self.assertEqual("", node.resolve(self.bot, "testid"))

        conversation = Conversation("testid", self.bot)
        question = Question.create_from_text("Hello world")
        question.current_sentence()._response = "Hello matey"
        conversation.record_dialog(question)
        question = Question.create_from_text("How are you")
        question.current_sentence()._response = "Very well thanks"
        conversation.record_dialog(question)
        self.bot._conversations["testid"] = conversation

        self.assertEqual("Very well thanks", node.resolve(self.bot, "testid"))


    def test_node_no_defaults(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateThatNode(position=1, index=1)
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)
        self.assertEqual(1, node.index)
        self.assertEqual(1, node.position)

        # Text that with no bot and therefore no conversation, "" is returned
        self.assertEqual("", node.resolve(None, None))

        conversation = Conversation("testid", self.bot)
        question = Question.create_from_text("Hello world")
        question.current_sentence()._response = "Hello matey"
        conversation.record_dialog(question)
        question = Question.create_from_text("How are you")
        question.current_sentence()._response = "Very well thanks"
        conversation.record_dialog(question)
        self.bot._conversations["testid"] = conversation

        self.assertEqual("Very well thanks", node.resolve(self.bot, "testid"))

    def test_to_xml_defaults(self):
        root = TemplateNode()
        node = TemplateThatNode()
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><that /></template>", xml_str)

    def test_to_xml_no_defaults(self):
        root = TemplateNode()
        node = TemplateThatNode(position=2, index=3)
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><that index="3" position="2" /></template>', xml_str)

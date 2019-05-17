import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.input import TemplateInputNode
from programy.dialog.conversation import Conversation
from programy.dialog.question import Question

from programytest.parser.base import ParserTestsBaseClass


class MockTemplateInputNode(TemplateInputNode):
    def __init__(self):
        TemplateInputNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")


class TemplateInputNodeTests(ParserTestsBaseClass):

    def test_to_str_defaults(self):
        node = TemplateInputNode()
        self.assertEqual("[INPUT[WORD]0]", node.to_string())

    def test_to_str_no_defaults(self):
        node = TemplateInputNode(index=2)
        self.assertEqual("[INPUT[WORD]2]", node.to_string())

    def test_to_xml_defaults(self):
        root = TemplateNode()
        node = TemplateInputNode()
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><input index="0" /></template>', xml_str)

    def test_to_xml_no_defaults(self):
        root = TemplateNode()
        node = TemplateInputNode(index=3)
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><input index="3" /></template>', xml_str)

    def test_resolve_with_defaults(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateInputNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)
        self.assertIsInstance(node.index, TemplateNode)

        conversation = Conversation(self._client_context)

        question = Question.create_from_text(self._client_context, "Hello world", self._client_context.bot.sentence_splitter)
        question.current_sentence()._response = "Hello matey"
        conversation.record_dialog(question)

        self._client_context.bot._conversation_mgr._conversations["testid"] = conversation

        response = root.resolve(self._client_context)
        self.assertIsNotNone(response)
        self.assertEqual(response, "Hello world")

    def test_resolve_no_defaults(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateInputNode(index=1)
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)
        self.assertIsInstance(node.index, TemplateNode)

        conversation = Conversation(self._client_context)

        question = Question.create_from_text(self._client_context, "Hello world")
        question.current_sentence()._response = "Hello matey"
        conversation.record_dialog(question)

        question = Question.create_from_text(self._client_context, "How are you. Are you well")
        question.current_sentence()._response = "Fine thanks"
        conversation.record_dialog(question)

        self._client_context.bot._conversation_mgr._conversations["testid"] = conversation

        response = root.resolve(self._client_context)
        self.assertIsNotNone(response)
        self.assertEqual(response, "Hello world")

    def test_resolve_no_sentence(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateInputNode(index=3)
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)
        self.assertIsInstance(node.index, TemplateNode)

        conversation = Conversation(self._client_context)

        question = Question.create_from_text(self._client_context, "Hello world", self._client_context.bot.sentence_splitter)
        question.current_sentence()._response = "Hello matey"
        conversation.record_dialog(question)

        question = Question.create_from_text(self._client_context, "How are you. Are you well", self._client_context.bot.sentence_splitter)
        question.current_sentence()._response = "Fine thanks"
        conversation.record_dialog(question)

        self._client_context.bot._conversation_mgr._conversations["testid"] = conversation

        response = root.resolve(self._client_context)
        self.assertIsNotNone(response)
        self.assertEqual(response, "")

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateInputNode()
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)
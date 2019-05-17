import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.response import TemplateResponseNode
from programy.dialog.conversation import Conversation
from programy.dialog.question import Question

from programytest.parser.base import ParserTestsBaseClass


class MockTemplateResponseNode(TemplateResponseNode):
    def __init__(self):
        TemplateResponseNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")

class TemplateResponseNodeTests(ParserTestsBaseClass):

    def test_to_str_defaults(self):
        node = TemplateResponseNode()
        self.assertEqual("[RESPONSE[WORD]1]", node.to_string())

    def test_to_str_no_defaults(self):
        node = TemplateResponseNode(index=2)
        self.assertEqual("[RESPONSE[WORD]2]", node.to_string())

    def test_to_xml_defaults(self):
        root = TemplateNode()
        node = TemplateResponseNode()
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><response index="1" /></template>', xml_str)

    def test_to_xml_no_defaults(self):
        root = TemplateNode()
        node = TemplateResponseNode(index=3)
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><response index="3" /></template>', xml_str)

    def test_resolve_with_defaults(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateResponseNode()
        self.assertIsNotNone(node)
        self.assertIsInstance(node.index, TemplateNode)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = Conversation(self._client_context)

        question = Question.create_from_text(self._client_context, "Hello1 question")
        question.current_sentence()._response = "Hello1 response"
        conversation.record_dialog(question)

        question = Question.create_from_text(self._client_context, "Hello quesiton2")
        question.current_sentence()._response = "Hello2 response"
        conversation.record_dialog(question)

        self._client_context.bot._conversation_mgr._conversations["testid"] = conversation

        response = root.resolve(self._client_context)
        self.assertIsNotNone(response)
        self.assertEqual(response, "Hello1 response")

    def test_resolve_with_no_defaults(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateResponseNode(index=1)
        self.assertIsNotNone(node)
        self.assertIsInstance(node.index, TemplateNode)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = Conversation(self._client_context)

        question = Question.create_from_text(self._client_context, "Hello1 question")
        question.current_sentence()._response = "Hello1 response"
        conversation.record_dialog(question)

        question = Question.create_from_text(self._client_context, "Hello quesiton2")
        question.current_sentence()._response = "Hello2 response"
        conversation.record_dialog(question)

        self._client_context.bot._conversation_mgr._conversations["testid"] = conversation

        response = root.resolve(self._client_context)
        self.assertIsNotNone(response)
        self.assertEqual(response, "Hello1 response")

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateResponseNode()
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)
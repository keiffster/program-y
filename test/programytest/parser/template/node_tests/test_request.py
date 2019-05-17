import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.request import TemplateRequestNode
from programy.dialog.conversation import Conversation
from programy.dialog.question import Question

from programytest.parser.base import ParserTestsBaseClass


class MockTemplateRequestNode(TemplateRequestNode):
    def __init__(self):
        TemplateRequestNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")


class TemplateRequestNodeTests(ParserTestsBaseClass):

    def test_to_str_defaults(self):
        node = TemplateRequestNode()
        self.assertEqual("[REQUEST[WORD]1]", node.to_string())

    def test_to_str_no_defaults(self):
        node = TemplateRequestNode(index=2)
        self.assertEqual("[REQUEST[WORD]2]", node.to_string())

    def test_to_xml_defaults(self):
        root = TemplateNode()
        node = TemplateRequestNode()
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><request index="1" /></template>', xml_str)

    def test_to_xml_no_defaults(self):
        root = TemplateNode()
        node = TemplateRequestNode(index=3)
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><request index="3" /></template>', xml_str)

    def test_resolve_with_defaults(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateRequestNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)
        self.assertEqual("1", node.index.word)

        conversation = Conversation(self._client_context)
        self._client_context.bot._conversation_mgr._conversations["testid"] = conversation

        question = Question.create_from_text(self._client_context, "Hello world")
        question.current_sentence()._response = "Hello matey"
        conversation._questions.append(question)

        question = Question.create_from_text(self._client_context, "What did you say")
        question.current_sentence()._response = "Hello matey"
        conversation._questions.append(question)

        response = root.resolve(self._client_context)
        self.assertIsNotNone(response)
        self.assertEqual(response, "Hello world")

    def test_resolve_with_no_defaults(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateRequestNode(index=1)
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)
        self.assertEqual("1", node.index.word)

        conversation = Conversation(self._client_context)
        self._client_context.bot._conversation_mgr._conversations["testid"] = conversation

        question = Question.create_from_text(self._client_context, "Hello world")
        question.current_sentence()._response = "Hello matey"
        conversation._questions.append(question)

        question = Question.create_from_text(self._client_context, "What did you say")
        question.current_sentence()._response = "Hello matey"
        conversation._questions.append(question)

        response = root.resolve(self._client_context)
        self.assertIsNotNone(response)
        self.assertEqual(response, "Hello world")

    def test_resolve_no_sentence(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateRequestNode(index=3)
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)
        self.assertEqual("3", node.index.word)

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
        self.assertEqual(response, "")

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateRequestNode()
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)
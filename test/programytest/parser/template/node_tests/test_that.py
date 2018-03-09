import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.that import TemplateThatNode
from programy.dialog.dialog import Conversation, Question

from programytest.parser.base import ParserTestsBaseClass

class MockTemplateThatNode(TemplateThatNode):
    def __init__(self):
        TemplateThatNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")

class TemplateThatNodeTests(ParserTestsBaseClass):

    def test_to_str_defaults(self):
        node = TemplateThatNode()
        self.assertEquals("THAT", node.to_string())

    def test_to_str_no_defaults(self):
        node = TemplateThatNode(3, 2)
        self.assertEquals("THAT question=3 sentence=2", node.to_string())

    def test_to_str_star(self):
        node = TemplateThatNode(1, -1)
        self.assertEquals("THAT sentence=*", node.to_string())

    def test_to_xml_defaults(self):
        root = TemplateNode()
        node = TemplateThatNode()
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><that /></template>", xml_str)

    def test_to_xml_no_defaults(self):
        root = TemplateNode()
        node = TemplateThatNode(question=3, sentence=2)
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><that index="3,2" /></template>', xml_str)

    def test_to_xml_no_default_star(self):
        root = TemplateNode()
        node = TemplateThatNode(question=3, sentence=-1)
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><that index="3,*" /></template>', xml_str)

    def test_resolve_with_defaults(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateThatNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)
        self.assertEqual(1, node.question)
        self.assertEqual(1, node.sentence)

        conversation = Conversation(self._client_context)

        question = Question.create_from_text(self._client_context.brain.tokenizer, "Hello world")
        question.current_sentence()._response = "Hello matey"
        conversation.record_dialog(question)

        question = Question.create_from_text(self._client_context.brain.tokenizer, "How are you")
        question.current_sentence()._response = "Very well thanks"
        conversation.record_dialog(question)

        self._client_context.bot._conversations["testid"] = conversation

        self.assertEqual("Hello matey", node.resolve(self._client_context))

    def test_resolve_with_no_defaults(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateThatNode(question=1, sentence=1)
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)
        self.assertEqual(1, node.question)
        self.assertEqual(1, node.sentence)

        conversation = Conversation(self._client_context)

        question = Question.create_from_text(self._client_context.brain.tokenizer, "Hello world")
        question.current_sentence()._response = "Hello matey"
        conversation.record_dialog(question)

        question = Question.create_from_text(self._client_context.brain.tokenizer, "How are you")
        question.current_sentence()._response = "Very well thanks"
        conversation.record_dialog(question)

        self._client_context.bot._conversations["testid"] = conversation

        self.assertEqual("Hello matey", node.resolve(self._client_context))

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateThatNode()
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEquals("", result)
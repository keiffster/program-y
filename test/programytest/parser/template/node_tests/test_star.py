import xml.etree.ElementTree as ET

from programy.parser.template.nodes.star import TemplateStarNode
from programy.dialog.conversation import Conversation
from programy.dialog.question import Question
from programy.parser.pattern.matchcontext import MatchContext
from programy.parser.pattern.match import Match
from programy.parser.pattern.nodes.oneormore import PatternOneOrMoreWildCardNode
from programy.parser.template.nodes.base import TemplateNode

from programytest.parser.base import ParserTestsBaseClass

class MockTemplateStarNode(TemplateStarNode):
    def __init__(self):
        TemplateStarNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")


class TemplateStarNodeTests(ParserTestsBaseClass):

    def test_node_defaults(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateStarNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

    def test_node_no_conversation(self):
        root = TemplateNode()
        node = TemplateStarNode()
        root.append(node)

        self.assertEqual("", root.resolve(self._client_context))

    def test_node_no_question(self):
        root = TemplateNode()
        node = TemplateStarNode()
        root.append(node)

        conversation = Conversation(self._client_context)
        self._client_context.bot._conversation_mgr._conversations["testid"] = conversation

        self.assertEqual("", root.resolve(self._client_context))

    def test_node_no_sentences(self):
        root = TemplateNode()
        node = TemplateStarNode()
        root.append(node)

        conversation = Conversation(self._client_context)
        question = Question()
        conversation.record_dialog(question)
        self._client_context.bot._conversation_mgr._conversations["testid"] = conversation

        self.assertEqual("", root.resolve(self._client_context))

    def test_node_no_star(self):
        root = TemplateNode()
        node = TemplateStarNode()
        root.append(node)

        conversation = Conversation(self._client_context)
        question = Question.create_from_text(self._client_context, "Hello world")
        question.current_sentence()._response = "Hello matey"
        conversation.record_dialog(question)
        question = Question.create_from_text(self._client_context, "How are you")
        question.current_sentence()._response = "Very well thanks"
        conversation.record_dialog(question)
        self._client_context.bot._conversation_mgr._conversations["testid"] = conversation

        self.assertEqual("", root.resolve(self._client_context))

    def test_node_with_star(self):
        root = TemplateNode()
        node = TemplateStarNode()
        root.append(node)

        conversation = Conversation(self._client_context)
        question = Question.create_from_text(self._client_context, "Hello world")
        question.current_sentence()._response = "Hello matey"
        conversation.record_dialog(question)
        question = Question.create_from_text(self._client_context, "How are you")
        question.current_sentence()._response = "Very well thanks"
        conversation.record_dialog(question)
        match = PatternOneOrMoreWildCardNode("*")
        context = MatchContext(max_search_depth=100, max_search_timeout=-1)
        context.add_match(Match(Match.WORD, match, "Matched"))
        question.current_sentence()._matched_context = context

        conversation.record_dialog(question)
        self._client_context.bot._conversation_mgr._conversations["testid"] = conversation

        self.assertEqual("Matched", root.resolve(self._client_context))

    def test_to_xml_defaults(self):
        root = TemplateNode()
        node = TemplateStarNode()
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><star index="1" /></template>', xml_str)

    def test_node_no_defaults(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateStarNode(index=2)
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)
        self.assertEqual("2", node.index.word)

    def test_to_xml_no_defaults(self):
        root = TemplateNode()
        node = TemplateStarNode(index=3)
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><star index="3" /></template>', xml_str)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateStarNode()
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)
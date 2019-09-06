import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.thatstar import TemplateThatStarNode
from programy.dialog.conversation import Conversation
from programy.dialog.question import Question
from programy.parser.pattern.matchcontext import MatchContext
from programy.parser.pattern.match import Match
from programy.parser.pattern.nodes.oneormore import PatternOneOrMoreWildCardNode

from programytest.parser.base import ParserTestsBaseClass

class MockTemplateThatStarNode(TemplateThatStarNode):
    def __init__(self):
        TemplateThatStarNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")


class TemplateThatStarNodeTests(ParserTestsBaseClass):

    def test_to_str_defaults(self):
        node = TemplateThatStarNode()
        self.assertEqual("[THATSTAR[WORD]1]", node.to_string())

    def test_to_str_no_defaults(self):
        node = TemplateThatStarNode("3,2")
        self.assertEqual("[THATSTAR[WORD]3,2]", node.to_string())

    def test_to_str_star(self):
        node = TemplateThatStarNode("1,*")
        self.assertEqual("[THATSTAR[WORD]1,*]", node.to_string())

    def test_to_xml_defaults(self):
        root = TemplateNode()
        node = TemplateThatStarNode()
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><thatstar index="1" /></template>', xml_str)

    def test_to_xml_no_defaults(self):
        root = TemplateNode()
        node = TemplateThatStarNode(index="3")
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><thatstar index="3" /></template>', xml_str)

    def test_to_xml_no_default_star(self):
        root = TemplateNode()
        node = TemplateThatStarNode("3")
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><thatstar index="3" /></template>', xml_str)

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateThatStarNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)
        self.assertIsInstance(node.index, TemplateNode)

    def test_node_no_defaults(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateThatStarNode(index="2,3")
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)
        self.assertIsInstance(node.index, TemplateNode)

    def test_node_no_star(self):
        root = TemplateNode()
        node = TemplateThatStarNode()
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
        node = TemplateThatStarNode()
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
        context.add_match(Match(Match.THAT, match, "Matched"))
        question.current_sentence()._matched_context = context
        conversation.record_dialog(question)

        self._client_context.bot._conversation_mgr._conversations["testid"] = conversation

        self.assertEqual("Matched", root.resolve(self._client_context))

    def test_node_with_star_with_none(self):
        root = TemplateNode()
        node = TemplateThatStarNode()
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
        context.add_match(Match(Match.THAT, match, None))
        question.current_sentence()._matched_context = context

        conversation.record_dialog(question)
        self._client_context.bot._conversation_mgr._conversations["testid"] = conversation

        self.assertEqual("", root.resolve(self._client_context))

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateThatStarNode()
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)
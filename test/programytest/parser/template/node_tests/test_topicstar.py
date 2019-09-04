import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.topicstar import TemplateTopicStarNode
from programy.dialog.conversation import Conversation
from programy.dialog.question import Question
from programy.parser.pattern.matchcontext import MatchContext
from programy.parser.pattern.match import Match
from programy.parser.pattern.nodes.oneormore import PatternOneOrMoreWildCardNode

from programytest.parser.base import ParserTestsBaseClass

class MockTemplateTopicStarNode(TemplateTopicStarNode):
    def __init__(self):
        TemplateTopicStarNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")

class TemplateNodeTests(ParserTestsBaseClass):

    def test_to_str_defaults(self):
        node = TemplateTopicStarNode()
        self.assertEqual("[TOPICSTAR[WORD]1]", node.to_string())

    def test_to_str_no_defaults(self):
        node = TemplateTopicStarNode(index=2)
        self.assertEqual("[TOPICSTAR[WORD]2]", node.to_string())

    def test_to_xml_defaults(self):
        root = TemplateNode()
        node = TemplateTopicStarNode()
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><topicstar index="1" /></template>', xml_str)

    def test_to_xml_no_defaults(self):
        root = TemplateNode()
        node = TemplateTopicStarNode(index=3)
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><topicstar index="3" /></template>', xml_str)

    def test_resolve_with_defaults_inside_topic(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateTopicStarNode()
        self.assertIsNotNone(node)
        self.assertIsInstance(node.index, TemplateNode)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = Conversation(self._client_context)

        question = Question.create_from_text(self._client_context, "Hello world", self._client_context.bot.sentence_splitter)
        question.current_sentence()._response = "Hello matey"
        conversation.record_dialog(question)

        question = Question.create_from_text(self._client_context, "How are you", self._client_context.bot.sentence_splitter)
        question.current_sentence()._response = "Very well thanks"
        conversation.record_dialog(question)

        match = PatternOneOrMoreWildCardNode("*")
        context = MatchContext(max_search_depth=100, max_search_timeout=-1)
        context.add_match(Match(Match.TOPIC, match, "Matched"))
        question.current_sentence()._matched_context = context
        conversation.record_dialog(question)

        self._client_context.bot._conversation_mgr._conversations["testid"] = conversation

        self.assertEqual("Matched", root.resolve(self._client_context))

    def test_resolve_no_defaults_inside_topic(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateTopicStarNode(index=1)
        self.assertIsNotNone(node)
        self.assertIsInstance(node.index, TemplateNode)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = Conversation(self._client_context)

        question = Question.create_from_text(self._client_context, "Hello world")
        question.current_sentence()._response = "Hello matey"
        conversation.record_dialog(question)

        question = Question.create_from_text(self._client_context, "How are you")
        question.current_sentence()._response = "Very well thanks"
        conversation.record_dialog(question)

        match = PatternOneOrMoreWildCardNode("*")
        context = MatchContext(max_search_depth=100, max_search_timeout=-1)
        context.add_match(Match(Match.TOPIC, match, "Matched"))
        question.current_sentence()._matched_context = context
        conversation.record_dialog(question)

        self._client_context.bot._conversation_mgr._conversations["testid"] = conversation

        self.assertEqual("Matched", node.resolve(self._client_context))

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateTopicStarNode()
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)
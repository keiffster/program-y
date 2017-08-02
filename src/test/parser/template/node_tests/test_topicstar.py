import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.topicstar import TemplateTopicStarNode
from programy.dialog import Conversation, Question
from programy.parser.pattern.matcher import MatchContext, Match
from programy.parser.pattern.nodes.oneormore import PatternOneOrMoreWildCardNode

from test.parser.template.base import TemplateTestsBaseClass


class TemplateTopicStarNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateTopicStarNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

    def test_to_xml_defaults(self):
        root = TemplateNode()
        node = TemplateTopicStarNode()
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><topicstar /></template>", xml_str)

    def test_node_no_defaults(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateTopicStarNode(position=3, index=2)
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)
        self.assertEqual(2, node.index)
        self.assertEqual(3, node.position)

    def test_node_no_star(self):
        root = TemplateNode()
        node = TemplateTopicStarNode()
        root.append(node)

        conversation = Conversation("testid", self.bot)
        question = Question.create_from_text("Hello world")
        question.current_sentence()._response = "Hello matey"
        conversation.record_dialog(question)
        question = Question.create_from_text("How are you")
        question.current_sentence()._response = "Very well thanks"
        conversation.record_dialog(question)
        self.bot._conversations["testid"] = conversation

        self.assertEqual("", root.resolve(self.bot, self.clientid))

    def test_node_with_star(self):
        root = TemplateNode()
        node = TemplateTopicStarNode()
        root.append(node)

        conversation = Conversation("testid", self.bot)
        question = Question.create_from_text("Hello world")
        question.current_sentence()._response = "Hello matey"
        conversation.record_dialog(question)
        question = Question.create_from_text("How are you")
        question.current_sentence()._response = "Very well thanks"
        conversation.record_dialog(question)
        match = PatternOneOrMoreWildCardNode("*")
        context = MatchContext(max_search_depth=100, max_search_timeout=-1)
        context.add_match(Match(Match.TOPIC, match, "Matched"))
        question.current_sentence()._matched_context = context

        conversation.record_dialog(question)
        self.bot._conversations["testid"] = conversation

        self.assertEqual("Matched", root.resolve(self.bot, self.clientid))

    def test_node_with_star_with_none(self):
        root = TemplateNode()
        node = TemplateTopicStarNode()
        root.append(node)

        conversation = Conversation("testid", self.bot)
        question = Question.create_from_text("Hello world")
        question.current_sentence()._response = "Hello matey"
        conversation.record_dialog(question)
        question = Question.create_from_text("How are you")
        question.current_sentence()._response = "Very well thanks"
        conversation.record_dialog(question)
        match = PatternOneOrMoreWildCardNode("*")
        context = MatchContext(max_search_depth=100, max_search_timeout=-1)
        context.add_match(Match(Match.TOPIC, match, None))
        question.current_sentence()._matched_context = context

        conversation.record_dialog(question)
        self.bot._conversations["testid"] = conversation

        self.assertEqual("", root.resolve(self.bot, self.clientid))

    def test_to_xml_no_defaults(self):
        root = TemplateNode()
        node = TemplateTopicStarNode(position=2, index=3)
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><topicstar index="3" position="2" /></template>', xml_str)

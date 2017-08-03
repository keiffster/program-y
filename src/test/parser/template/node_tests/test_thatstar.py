import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.thatstar import TemplateThatStarNode
from programy.dialog import Conversation, Question
from programy.parser.pattern.matcher import MatchContext, Match
from programy.parser.pattern.nodes.oneormore import PatternOneOrMoreWildCardNode

from test.parser.template.base import TemplateTestsBaseClass


class TemplateThatStarNodeTests(TemplateTestsBaseClass):

    def test_to_str_defaults(self):
        node = TemplateThatStarNode()
        self.assertEquals("THATSTAR", node.to_string())

    def test_to_str_no_defaults(self):
        node = TemplateThatStarNode(3, 2)
        self.assertEquals("THATSTAR question=3 sentence=2", node.to_string())

    def test_to_str_star(self):
        node = TemplateThatStarNode(1, -1)
        self.assertEquals("THATSTAR sentence=*", node.to_string())

    def test_to_xml_defaults(self):
        root = TemplateNode()
        node = TemplateThatStarNode()
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><thatstar /></template>", xml_str)

    def test_to_xml_no_defaults(self):
        root = TemplateNode()
        node = TemplateThatStarNode(question=3, sentence=2)
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><thatstar index="3,2" /></template>', xml_str)

    def test_to_xml_no_default_star(self):
        root = TemplateNode()
        node = TemplateThatStarNode(question=3, sentence=-1)
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><thatstar index="3,*" /></template>', xml_str)

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateThatStarNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)
        self.assertEquals(1, node.question)
        self.assertEquals(1, node.sentence)

    def test_node_no_defaults(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateThatStarNode(question=3, sentence=2)
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)
        self.assertEquals(3, node.question)
        self.assertEquals(2, node.sentence)

    def test_node_no_star(self):
        root = TemplateNode()
        node = TemplateThatStarNode()
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
        node = TemplateThatStarNode()
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
        context.add_match(Match(Match.THAT, match, "Matched"))
        question.current_sentence()._matched_context = context
        conversation.record_dialog(question)

        self.bot._conversations["testid"] = conversation

        self.assertEqual("Matched", root.resolve(self.bot, self.clientid))

    def test_node_with_star_with_none(self):
        root = TemplateNode()
        node = TemplateThatStarNode()
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
        context.add_match(Match(Match.THAT, match, None))
        question.current_sentence()._matched_context = context

        conversation.record_dialog(question)
        self.bot._conversations["testid"] = conversation

        self.assertEqual("", root.resolve(self.bot, self.clientid))


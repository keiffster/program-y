import xml.etree.ElementTree as ET

from programy.dialog.conversation import Conversation
from programy.dialog.question import Question
from programy.parser.exceptions import ParserException
from programy.parser.pattern.match import Match
from programy.parser.pattern.matchcontext import MatchContext
from programy.parser.pattern.nodes.oneormore import PatternOneOrMoreWildCardNode
from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.star import TemplateStarNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.template.nodes.xml import TemplateXMLNode
from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class MockTemplateXMLNode(TemplateXMLNode):

    def __init__(self):
        TemplateXMLNode.__init__(self)

    def _parse_attrib(self, graph, expression, attrib_name):
        raise Exception("Test Broken")


class TemplateGraphXMLTests(TemplateGraphTestClient):

    def test_basic_xml_node_from_xml(self):
        template = ET.fromstring("""
            <template>
                <dial>07777777</dial>
            </template>
            """)
        
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        xml_node = ast.children[0]
        self.assertIsNotNone(xml_node)
        self.assertIsInstance(xml_node, TemplateXMLNode)

        result = xml_node.resolve(self.create_client_context("testid"))
        self.assertIsNotNone(result)
        self.assertEqual(result, "<dial>07777777</dial>")

    def test_attrib_xml_node_from_xml(self):
        template = ET.fromstring("""
            <template>
                <dial leave_message="true">07777777</dial>
            </template>
            """)
        
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        xml_node = ast.children[0]
        self.assertIsNotNone(xml_node)
        self.assertIsInstance(xml_node, TemplateXMLNode)

        result = xml_node.resolve(self.create_client_context("testid"))
        self.assertIsNotNone(result)
        self.assertEqual(result, '<dial leave_message="true">07777777</dial>')

    def test_attrib_with_html(self):
        template = ET.fromstring("""
            <template>
                <a target="_new" href="http://www.google.com/search?q=&lt;star /&gt;"> Google Search </a>
            </template>
            """)

        conversation = Conversation(self._client_context)
        question = Question.create_from_text(self._client_context, "GOOGLE AIML", self._client_context.bot.sentence_splitter)
        question.current_sentence()._response = "OK"
        conversation.record_dialog(question)
        match = PatternOneOrMoreWildCardNode("*")
        context = MatchContext(max_search_depth=100, max_search_timeout=-1)
        context.add_match(Match(Match.WORD, match, "AIML"))
        question.current_sentence()._matched_context = context
        self._client_context.bot._conversation_mgr._conversations["testid"] = conversation

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        xml_node = ast.children[0]
        self.assertIsNotNone(xml_node)
        self.assertIsInstance(xml_node, TemplateXMLNode)

        attribs = xml_node.attribs
        self.assertEqual(2, len(attribs))

        self.assertIsInstance(attribs['target'], TemplateWordNode)
        target = attribs['target']
        self.assertEqual(len(target.children), 0)
        self.assertEqual("_new", target.word)

        self.assertIsInstance(attribs['href'], TemplateNode)
        href = attribs['href']
        self.assertEqual(len(href.children), 3)

        self.assertIsInstance(href.children[0], TemplateWordNode)
        self.assertEqual('http://www.google.com/search?q=', href.children[0].word)

        self.assertIsInstance(href.children[1], TemplateNode)
        self.assertEqual(1, len(href.children[1].children))
        star = href.children[1].children[0]
        self.assertIsInstance(star, TemplateStarNode)

        self.assertIsInstance(href.children[2], TemplateWordNode)
        self.assertEqual('', href.children[2].word)

        result = xml_node.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual(result, '<a target="_new" href="http://www.google.com/search?q=AIML">Google Search</a>')

    def test_parse_invalid_attribs(self):
        template = ET.fromstring("""
                <dial std="44">07777777</dial>
            """)

        xml = MockTemplateXMLNode()

        with self.assertRaises(ParserException):
            xml._parse_node_with_xml_attribs(self._graph, template)

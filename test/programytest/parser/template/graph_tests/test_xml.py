import xml.etree.ElementTree as ET

from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.template.nodes.xml import TemplateXMLNode
from programy.parser.template.nodes.star import TemplateStarNode
from programy.dialog.conversation import Conversation
from programy.dialog.question import Question
from programy.parser.pattern.matchcontext import MatchContext
from programy.parser.pattern.match import Match
from programy.parser.pattern.nodes.oneormore import PatternOneOrMoreWildCardNode
from programy.parser.template.nodes.base import TemplateNode

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


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
        self.assertEquals(result, "<dial>07777777</dial>")

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
        self.assertEquals(result, '<dial leave_message="true">07777777</dial>')

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
        self.assertEquals(2, len(attribs))

        self.assertIsInstance(attribs['target'], TemplateWordNode)
        target = attribs['target']
        self.assertEquals(len(target.children), 0)
        self.assertEquals("_new", target.word)

        self.assertIsInstance(attribs['href'], TemplateNode)
        href = attribs['href']
        self.assertEquals(len(href.children), 3)

        self.assertIsInstance(href.children[0], TemplateWordNode)
        self.assertEquals('http://www.google.com/search?q=', href.children[0].word)

        self.assertIsInstance(href.children[1], TemplateNode)
        self.assertEquals(1, len(href.children[1].children))
        star = href.children[1].children[0]
        self.assertIsInstance(star, TemplateStarNode)

        self.assertIsInstance(href.children[2], TemplateWordNode)
        self.assertEquals('', href.children[2].word)

        result = xml_node.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEquals(result, '<a target="_new" href="http://www.google.com/search?q=AIML">Google Search</a>')

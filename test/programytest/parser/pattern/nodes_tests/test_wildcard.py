from programytest.parser.base import ParserTestsBaseClass

from programy.parser.exceptions import ParserException
from programy.parser.pattern.nodes.wildcard import PatternWildCardNode
from programy.parser.pattern.nodes.zeroormore import PatternZeroOrMoreWildCardNode
from programy.parser.pattern.nodes.oneormore import PatternOneOrMoreWildCardNode
from programy.parser.pattern.nodes.word import PatternWordNode
from programy.parser.pattern.nodes.root import PatternRootNode
from programy.parser.pattern.nodes.topic import PatternTopicNode
from programy.parser.template.nodes.base import TemplateNode
from programy.parser.pattern.nodes.template import PatternTemplateNode
from programy.parser.pattern.matchcontext import MatchContext
from programy.parser.pattern.match import Match
from programy.dialog.sentence import Sentence


class MockPatternWildCardNode(PatternWildCardNode):

    def __init__(self, wildcard):
        PatternWildCardNode.__init__(self, wildcard)

    def matching_wildcards(self):
        return ["*"]


class PatternWildCardNodeTests(ParserTestsBaseClass):

    def test_wildcard(self):

        wildcard = MockPatternWildCardNode("*")
        self.assertIsNotNone(wildcard)

        self.assertTrue(wildcard.is_wildcard())

        with self.assertRaises(ParserException):
            wildcard.can_add(PatternRootNode())

        wildcard.can_add(PatternWordNode("test"))

        self.assertEqual(["*"], wildcard.matching_wildcards())

    def test_invalid_topic_or_that(self):

        wildcard = MockPatternWildCardNode("*")
        self.assertIsNotNone(wildcard)

        context = MatchContext(max_search_depth=100, max_search_timeout=-1)
        matches_added = 1

        self.assertTrue(wildcard.invalid_topic_or_that("", self._client_context, PatternTopicNode.TOPIC, context, matches_added))
        self.assertTrue(wildcard.invalid_topic_or_that("", self._client_context, PatternTopicNode.THAT, context, matches_added))

        self.assertFalse(wildcard.invalid_topic_or_that("", self._client_context, "TEST", context, matches_added))

    def test_check_child_is_wildcard_no_wildcard_children(self):

        wildcard = MockPatternWildCardNode("*")
        self.assertIsNotNone(wildcard)

        context = MatchContext(max_search_depth=100, max_search_timeout=-1)
        sentence = Sentence(self._client_context, "TEST SENTENCE")
        match = wildcard.check_child_is_wildcard("", self._client_context, context, sentence, 0,  Match.WORD, 0)
        self.assertIsNone(match)

    def test_check_child_is_wildcard_hash(self):

        wildcard = MockPatternWildCardNode("*")
        self.assertIsNotNone(wildcard)
        wildcard._0ormore_hash = PatternZeroOrMoreWildCardNode('#')
        wildcard._0ormore_hash._template = PatternTemplateNode(TemplateNode())

        context = MatchContext(max_search_depth=100, max_search_timeout=-1)
        sentence = Sentence(self._client_context, "TEST SENTENCE")
        match = wildcard.check_child_is_wildcard("", self._client_context, context, sentence, 0,  Match.WORD, 0)
        self.assertIsNotNone(match)

        context = MatchContext(max_search_depth=100, max_search_timeout=-1)
        sentence = Sentence(self._client_context, "TEST")
        match = wildcard.check_child_is_wildcard("", self._client_context, context, sentence, 0,  Match.WORD, 0)
        self.assertIsNotNone(match)

    def test_check_child_is_wildcard_arrow(self):

        wildcard = MockPatternWildCardNode("*")
        self.assertIsNotNone(wildcard)
        wildcard._0ormore_arrow = PatternZeroOrMoreWildCardNode('^')
        wildcard._0ormore_arrow._template = PatternTemplateNode(TemplateNode())

        context = MatchContext(max_search_depth=100, max_search_timeout=-1)
        sentence = Sentence(self._client_context, "TEST SENTENCE")
        match = wildcard.check_child_is_wildcard("", self._client_context, context, sentence, 0,  Match.WORD, 0)
        self.assertIsNotNone(match)

        context = MatchContext(max_search_depth=100, max_search_timeout=-1)
        sentence = Sentence(self._client_context, "TEST")
        match = wildcard.check_child_is_wildcard("", self._client_context, context, sentence, 0,  Match.WORD, 0)
        self.assertIsNotNone(match)

    def test_check_child_is_wildcard_star(self):

        wildcard = MockPatternWildCardNode("*")
        self.assertIsNotNone(wildcard)
        wildcard._1ormore_star = PatternOneOrMoreWildCardNode('*')
        wildcard._1ormore_star._template = PatternTemplateNode(TemplateNode())

        context = MatchContext(max_search_depth=100, max_search_timeout=-1)
        sentence = Sentence(self._client_context, "TEST SENTENCE")
        match = wildcard.check_child_is_wildcard("", self._client_context, context, sentence, 0,  Match.WORD, 0)
        self.assertIsNotNone(match)

        context = MatchContext(max_search_depth=100, max_search_timeout=-1)
        sentence = Sentence(self._client_context, "TEST")
        match = wildcard.check_child_is_wildcard("", self._client_context, context, sentence, 0, Match.WORD, 0)
        self.assertIsNone(match)

    def test_check_child_is_wildcard_underline(self):

        wildcard = MockPatternWildCardNode("*")
        self.assertIsNotNone(wildcard)
        wildcard._1ormore_underline = PatternOneOrMoreWildCardNode('_')
        wildcard._1ormore_underline._template = PatternTemplateNode(TemplateNode())

        context = MatchContext(max_search_depth=100, max_search_timeout=-1)
        sentence = Sentence(self._client_context, "TEST SENTENCE")
        match = wildcard.check_child_is_wildcard("", self._client_context, context, sentence, 0,  Match.WORD, 0)
        self.assertIsNotNone(match)

        context = MatchContext(max_search_depth=100, max_search_timeout=-1)
        sentence = Sentence(self._client_context, "TEST")
        match = wildcard.check_child_is_wildcard("", self._client_context, context, sentence, 0,  Match.WORD, 0)
        self.assertIsNone(match)


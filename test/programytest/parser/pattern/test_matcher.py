import unittest
import datetime

from programy.parser.pattern.matcher import Match
from programy.parser.pattern.matcher import MatchContext
from programy.parser.pattern.matcher import EqualsMatch
from programy.parser.pattern.nodes.oneormore import PatternOneOrMoreWildCardNode
from programy.parser.pattern.nodes.template import PatternTemplateNode
from programy.parser.template.nodes.base import TemplateNode
from programytest.client import TestClient


class MatcherTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(MatcherTestClient, self).load_storage()
        self.add_default_stores()
        self.add_pattern_nodes_store()
        

class PatternFactoryTests(unittest.TestCase):

    def setUp(self):
        client = MatcherTestClient()
        self._client_context = client.create_client_context("testid")
        
    def test_match_no_word(self):
        topic = PatternOneOrMoreWildCardNode("*")
        match = Match(Match.TOPIC, topic, None)
        self.assertEqual(Match.TOPIC, match.match_type)
        self.assertEqual(topic, match.matched_node)
        self.assertEqual([], match.matched_words)
        self.assertEqual("Match=(Topic) Node=(ONEORMORE [*]) Matched=()", match.to_string(self._client_context.brain.tokenizer))

    def test_match_word(self):
        topic = PatternOneOrMoreWildCardNode("*")
        match = Match(Match.TOPIC, topic, "Hello")
        self.assertEqual(Match.TOPIC, match.match_type)
        self.assertEqual(topic, match.matched_node)
        self.assertEqual(["Hello"], match.matched_words)
        self.assertEqual("Match=(Topic) Node=(ONEORMORE [*]) Matched=(Hello)", match.to_string(self._client_context.brain.tokenizer))

    def test_match_multi_word(self):
        topic = PatternOneOrMoreWildCardNode("*")
        match = Match(Match.TOPIC, topic, None)
        match.add_word("Hello")
        match.add_word("World")
        self.assertEqual(["Hello", "World"], match.matched_words)
        self.assertEqual("Hello World", match.joined_words(self._client_context.brain.tokenizer))
        self.assertEqual("Match=(Topic) Node=(ONEORMORE [*]) Matched=(Hello World)", match.to_string(self._client_context.brain.tokenizer))

    def test_type_to_string(self):
        self.assertEqual("Word", Match.type_to_string(Match.WORD))
        self.assertEqual("Topic", Match.type_to_string(Match.TOPIC))
        self.assertEqual("That", Match.type_to_string(Match.THAT))
        self.assertEqual("Unknown", Match.type_to_string(999))

    def test_match_context_depth(self):
        context1 = MatchContext(max_search_depth=100, max_search_timeout=60, tokenizer=self._client_context.brain.tokenizer)
        self.assertEqual(100, context1.max_search_depth)
        self.assertEqual(60, context1.max_search_time)

    def test_match_context_depth(self):
        context = MatchContext(max_search_depth=100, max_search_timeout=60, tokenizer=self._client_context.brain.tokenizer)
        self.assertEqual(100, context.max_search_depth)
        self.assertEqual(60, context.max_search_timeout)
        self.assertFalse(context.matched())
        template = PatternTemplateNode(template=TemplateNode)
        context.set_template(template)
        self.assertEqual(template, context.template_node())
        self.assertTrue(context.matched())

    def test_match_context_pop_push(self):
        topic = PatternOneOrMoreWildCardNode("*")
        context = MatchContext(max_search_depth=100, max_search_timeout=60, tokenizer=self._client_context.brain.tokenizer)
        context.add_match(Match(Match.TOPIC, topic, None))
        self.assertEqual(1, len(context.matched_nodes))
        context.add_match(Match(Match.TOPIC, topic, None))
        self.assertEqual(2, len(context.matched_nodes))
        context.add_match(Match(Match.TOPIC, topic, None))
        self.assertEqual(3, len(context.matched_nodes))
        context.pop_match()
        self.assertEqual(2, len(context.matched_nodes))
        context.pop_match()
        self.assertEqual(1, len(context.matched_nodes))
        context.pop_match()
        self.assertEqual(0, len(context.matched_nodes))
        context.pop_match()
        self.assertEqual(0, len(context.matched_nodes))

    def test_match_context_star(self):
        word = PatternOneOrMoreWildCardNode("*")
        topic = PatternOneOrMoreWildCardNode("*")
        that = PatternOneOrMoreWildCardNode("*")

        context = MatchContext(max_search_depth=100, max_search_timeout=60, tokenizer=self._client_context.brain.tokenizer)

        context.add_match(Match(Match.WORD, word, "Hello"))
        context.add_match(Match(Match.TOPIC, topic, "Hello Topic"))
        context.add_match(Match(Match.THAT, that, "Hello That"))
        self.assertEqual(3, len(context.matched_nodes))

        self.assertEqual("Hello", context.star(1))
        self.assertIsNone(context.star(2))
        self.assertEqual("Hello Topic", context.topicstar(1))
        self.assertIsNone(context.topicstar(2))
        self.assertEqual("Hello That", context.thatstar(1))
        self.assertIsNone(context.thatstar(2))

    def test_equals_match(self):
        equals_match = EqualsMatch(True, 1, "Hello World")
        self.assertIsNotNone(equals_match)
        self.assertTrue(equals_match.matched)
        self.assertEqual(1, equals_match.word_no)
        self.assertEqual("Hello World", equals_match.matched_phrase)
        self.assertEqual("True, 1, Hello World", equals_match.to_string())

    def test_time_functions(self):
        context = MatchContext(max_search_depth=100, max_search_timeout=-1, tokenizer=self._client_context.brain.tokenizer)
        self.assertEqual(-1, context.max_search_timeout)
        self.assertFalse(context.search_time_exceeded())

        context = MatchContext(max_search_depth=100, max_search_timeout=0, tokenizer=self._client_context.brain.tokenizer)
        self.assertEqual(0, context.max_search_timeout)
        self.assertTrue(context.search_time_exceeded())

        context = MatchContext(max_search_depth=100, max_search_timeout=60, tokenizer=self._client_context.brain.tokenizer)
        time_now = datetime.datetime.now()
        prev_time = time_now - datetime.timedelta(seconds=-70)
        context._total_search_start = prev_time
        self.assertTrue(context.search_time_exceeded())

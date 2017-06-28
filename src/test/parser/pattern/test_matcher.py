import unittest

from programy.parser.pattern.matcher import Match
from programy.parser.pattern.matcher import MatchContext
from programy.parser.pattern.matcher import EqualsMatch
from programy.parser.pattern.nodes.oneormore import PatternOneOrMoreWildCardNode
from programy.parser.pattern.nodes.topic import PatternTopicNode
from programy.parser.pattern.nodes.that import PatternThatNode
from programy.parser.pattern.nodes.template import PatternTemplateNode
from programy.parser.template.nodes.base import TemplateNode

class PatternFactoryTests(unittest.TestCase):

    def test_match_no_word(self):
        topic = PatternOneOrMoreWildCardNode("*")
        match = Match(Match.TOPIC, topic, None)
        self.assertEquals(Match.TOPIC, match.match_type)
        self.assertEquals(topic, match.matched_node)
        self.assertEquals([], match.matched_words)
        self.assertEquals("Match=(Topic) Node=(ONEORMORE [*]) Matched=()", match.to_string())

    def test_match_word(self):
        topic = PatternOneOrMoreWildCardNode("*")
        match = Match(Match.TOPIC, topic, "Hello")
        self.assertEquals(Match.TOPIC, match.match_type)
        self.assertEquals(topic, match.matched_node)
        self.assertEquals(["Hello"], match.matched_words)
        self.assertEquals("Match=(Topic) Node=(ONEORMORE [*]) Matched=(Hello)", match.to_string())

    def test_match_multi_word(self):
        topic = PatternOneOrMoreWildCardNode("*")
        match = Match(Match.TOPIC, topic, None)
        match.add_word("Hello")
        match.add_word("World")
        self.assertEquals(["Hello", "World"], match.matched_words)
        self.assertEquals("Hello World", match.joined_words())
        self.assertEquals("Match=(Topic) Node=(ONEORMORE [*]) Matched=(Hello World)", match.to_string())

    def test_type_to_string(self):
        self.assertEquals("Word", Match.type_to_string(Match.WORD))
        self.assertEquals("Topic", Match.type_to_string(Match.TOPIC))
        self.assertEquals("That", Match.type_to_string(Match.THAT))
        self.assertEquals("Unknown", Match.type_to_string(999))

    def test_match_context_depth(self):
        context1 = MatchContext()
        self.assertEquals(MatchContext.MAX_SEARCH_DEPTH, context1.max_search_depth)

        context2 = MatchContext(999)
        self.assertEquals(999, context2.max_search_depth)

    def test_match_context_depth(self):
        context = MatchContext()
        self.assertFalse(context.matched())
        template = PatternTemplateNode(template=TemplateNode)
        context.set_template(template)
        self.assertEquals(template, context.template_node())
        self.assertTrue(context.matched())

    def test_match_context_pop_push(self):
        topic = PatternOneOrMoreWildCardNode("*")
        context = MatchContext()
        context.add_match(Match(Match.TOPIC, topic, None))
        self.assertEquals(1, len(context.matched_nodes))
        context.add_match(Match(Match.TOPIC, topic, None))
        self.assertEquals(2, len(context.matched_nodes))
        context.add_match(Match(Match.TOPIC, topic, None))
        self.assertEquals(3, len(context.matched_nodes))
        context.pop_match()
        self.assertEquals(2, len(context.matched_nodes))
        context.pop_match()
        self.assertEquals(1, len(context.matched_nodes))
        context.pop_match()
        self.assertEquals(0, len(context.matched_nodes))
        context.pop_match()
        self.assertEquals(0, len(context.matched_nodes))

    def test_match_context_star(self):
        word = PatternOneOrMoreWildCardNode("*")
        topic = PatternOneOrMoreWildCardNode("*")
        that = PatternOneOrMoreWildCardNode("*")

        context = MatchContext()

        context.add_match(Match(Match.WORD, word, "Hello"))
        context.add_match(Match(Match.TOPIC, topic, "Hello Topic"))
        context.add_match(Match(Match.THAT, that, "Hello That"))
        self.assertEquals(3, len(context.matched_nodes))

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
        self.assertEquals(1, equals_match.word_no)
        self.assertEquals("Hello World", equals_match.matched_phrase)
        self.assertEquals("True, 1, Hello World", equals_match.to_string())
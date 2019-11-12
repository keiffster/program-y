from programy.dialog.sentence import Sentence
from programy.parser.exceptions import ParserException
from programy.parser.pattern.match import Match
from programy.parser.pattern.matchcontext import MatchContext
from programy.parser.pattern.nodes.priority import PatternPriorityWordNode
from programy.parser.pattern.nodes.template import PatternTemplateNode
from programy.parser.pattern.nodes.that import PatternThatNode
from programy.parser.pattern.nodes.topic import PatternTopicNode
from programy.parser.pattern.nodes.word import PatternWordNode
from programy.parser.pattern.nodes.zeroormore import PatternZeroOrMoreWildCardNode
from programy.parser.template.nodes.word import TemplateWordNode
from programytest.parser.base import ParserTestsBaseClass


class PatternZeroOrMoreWildCardNodeTests(ParserTestsBaseClass):

    def test_invalid_wildcard(self):
        with self.assertRaises(ParserException) as raised:
            node = PatternZeroOrMoreWildCardNode("X")
            self.assertIsNone(node)

    def test_hash(self):
        node = PatternZeroOrMoreWildCardNode("#")

        self.assertFalse(node.is_root())
        self.assertFalse(node.is_priority())
        self.assertTrue(node.is_zero_or_more())
        self.assertFalse(node.is_one_or_more())
        self.assertFalse(node.is_set())
        self.assertFalse(node.is_bot())
        self.assertFalse(node.is_template())
        self.assertFalse(node.is_that())
        self.assertFalse(node.is_topic())
        self.assertTrue(node.is_wildcard())

        self.assertIsNotNone(node.children)
        self.assertFalse(node.has_children())

        sentence = Sentence(self._client_context, "*")

        self.assertEqual(node.wildcard, "#")
        self.assertTrue(node.equivalent(PatternZeroOrMoreWildCardNode("#")))
        result = node.equals(self._client_context, sentence, 0)
        self.assertFalse(result.matched)
        self.assertEqual(node.to_string(), "ZEROORMORE [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] wildcard=[#]")
        self.assertEqual('<zerormore wildcard="#">\n</zerormore>\n', node.to_xml(self._client_context))

        self.assertFalse(node.equivalent(PatternWordNode("test")))

    def test_arrow(self):
        node = PatternZeroOrMoreWildCardNode("^")

        self.assertFalse(node.is_root())
        self.assertFalse(node.is_priority())
        self.assertTrue(node.is_zero_or_more())
        self.assertFalse(node.is_one_or_more())
        self.assertFalse(node.is_set())
        self.assertFalse(node.is_bot())
        self.assertFalse(node.is_template())
        self.assertFalse(node.is_that())
        self.assertFalse(node.is_topic())
        self.assertTrue(node.is_wildcard())

        self.assertIsNotNone(node.children)
        self.assertFalse(node.has_children())

        sentence = Sentence(self._client_context, "*")

        self.assertEqual(node.wildcard, "^")
        self.assertTrue(node.equivalent(PatternZeroOrMoreWildCardNode("^")))
        result = node.equals(self._client_context, sentence, 0)
        self.assertFalse(result.matched)
        self.assertEqual(node.to_string(), "ZEROORMORE [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] wildcard=[^]")
        self.assertEqual('<zerormore wildcard="^">\n</zerormore>\n', node.to_xml(self._client_context))

        self.assertFalse(node.equivalent(PatternWordNode("test")))

    def test_to_xml(self):
        node1 = PatternZeroOrMoreWildCardNode("^")
        self.assertEqual('<zerormore wildcard="^">\n</zerormore>\n', node1.to_xml(self._client_context))
        self.assertEqual('<zerormore userid="*" wildcard="^">\n</zerormore>\n', node1.to_xml(self._client_context, include_user=True))

        node2 = PatternZeroOrMoreWildCardNode("^", userid="testid")
        self.assertEqual('<zerormore wildcard="^">\n</zerormore>\n', node2.to_xml(self._client_context))
        self.assertEqual('<zerormore userid="testid" wildcard="^">\n</zerormore>\n', node2.to_xml(self._client_context, include_user=True))

    def test_to_string(self):
        node1 = PatternZeroOrMoreWildCardNode("^")
        self.assertEqual("ZEROORMORE [^]", node1.to_string(verbose=False))
        self.assertEqual("ZEROORMORE [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] wildcard=[^]", node1.to_string(verbose=True))

        node1 = PatternZeroOrMoreWildCardNode("^", userid="testid")
        self.assertEqual("ZEROORMORE [^]", node1.to_string(verbose=False))
        self.assertEqual("ZEROORMORE [testid] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] wildcard=[^]", node1.to_string(verbose=True))

    def test_equivalent_userid(self):
        node1 = PatternZeroOrMoreWildCardNode("^")
        node2 = PatternZeroOrMoreWildCardNode("^")
        node3 = PatternZeroOrMoreWildCardNode("^", userid="testuser")

        self.assertTrue(node1.equivalent(node2))
        self.assertFalse(node1.equivalent(node3))

    def test_consume_search_time_exceeded(self):
        node = PatternZeroOrMoreWildCardNode("^")
        self.assertIsNotNone(node)

        match_context = MatchContext(max_search_depth=100, max_search_timeout=0)
        words = Sentence(self._client_context)

        result = node.consume(self._client_context, match_context, words, 0, Match.WORD, 1, parent=False)
        self.assertIsNone(result)

    def test_consume_search_depth_exceeded(self):
        node = PatternZeroOrMoreWildCardNode("^")
        self.assertIsNotNone(node)

        match_context = MatchContext(max_search_depth=0, max_search_timeout=100)
        words = Sentence(self._client_context)

        result = node.consume(self._client_context, match_context, words, 0, Match.WORD, 1, parent=False)
        self.assertIsNone(result)

    def test_consume_topic(self):
        node = PatternZeroOrMoreWildCardNode("^")
        self.assertIsNotNone(node)
        node.add_topic(PatternTopicNode())

        match_context = MatchContext(max_search_depth=100, max_search_timeout=100)
        words = Sentence(self._client_context, text="__TOPIC__")

        result = node.consume(self._client_context, match_context, words, 0, Match.WORD, 1, parent=False)
        self.assertIsNone(result)

    def test_consume_that(self):
        node = PatternZeroOrMoreWildCardNode("^")
        self.assertIsNotNone(node)
        node.add_that(PatternThatNode())

        match_context = MatchContext(max_search_depth=100, max_search_timeout=100)
        words = Sentence(self._client_context, text="__THAT__")

        result = node.consume(self._client_context, match_context, words, 0, Match.WORD, 1, parent=False)
        self.assertIsNone(result)

    def test_consume_with_priority(self):
        node = PatternZeroOrMoreWildCardNode("^")
        priority = PatternPriorityWordNode("$TEST")
        node.add_child(priority)
        priority.add_template((PatternTemplateNode(TemplateWordNode("word"))))

        match_context = MatchContext(max_search_depth=100, max_search_timeout=100)
        words = Sentence(self._client_context, text="THIS $TEST")

        result = node.consume(self._client_context, match_context, words, 0, Match.WORD, 1, parent=False)
        self.assertIsNotNone(result)

    def test_consume_with_priority_mismatch(self):
        node = PatternZeroOrMoreWildCardNode("^")
        priority = PatternPriorityWordNode("$TEST")
        node.add_child(priority)
        priority.add_template((PatternTemplateNode(TemplateWordNode("word"))))

        match_context = MatchContext(max_search_depth=100, max_search_timeout=100)
        words = Sentence(self._client_context, text="THIS $TEST2")

        result = node.consume(self._client_context, match_context, words, 0, Match.WORD, 1, parent=False)
        self.assertIsNone(result)

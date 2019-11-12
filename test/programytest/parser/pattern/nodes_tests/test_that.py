from programy.dialog.sentence import Sentence
from programy.parser.exceptions import ParserException
from programy.parser.pattern.match import Match
from programy.parser.pattern.matchcontext import MatchContext
from programy.parser.pattern.nodes.root import PatternRootNode
from programy.parser.pattern.nodes.that import PatternThatNode
from programy.parser.pattern.nodes.topic import PatternTopicNode
from programytest.parser.base import ParserTestsBaseClass


class PatternThatNodeTests(ParserTestsBaseClass):

    def test_init(self):
        node = PatternThatNode()
        self.assertIsNotNone(node)

        self.assertFalse(node.is_root())
        self.assertFalse(node.is_priority())
        self.assertFalse(node.is_wildcard())
        self.assertFalse(node.is_zero_or_more())
        self.assertFalse(node.is_one_or_more())
        self.assertFalse(node.is_set())
        self.assertFalse(node.is_bot())
        self.assertFalse(node.is_template())
        self.assertTrue(node.is_that())
        self.assertFalse(node.is_topic())
        self.assertFalse(node.is_wildcard())

        self.assertIsNotNone(node.children)
        self.assertFalse(node.has_children())

        self.assertTrue(node.equivalent(PatternThatNode()))
        self.assertEqual(node.to_string(), "THAT [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)]")
        self.assertEqual(node.to_string(verbose=False), "THAT")

        self.assertEqual("<that></that>\n", node.to_xml(self._client_context))

    def test_root_to_that(self):
        node1 = PatternThatNode()
        node2 = PatternRootNode()

        with self.assertRaises(ParserException) as raised:
            node1.can_add(node2)
        self.assertEqual(str(raised.exception), "Cannot add root node to that node")

    def test_topic_to_that(self):
        node1 = PatternThatNode()
        node2 = PatternTopicNode()

        with self.assertRaises(ParserException) as raised:
            node1.can_add(node2)
        self.assertEqual(str(raised.exception), "Cannot add topic node to that node")

    def test_that_to_that(self):
        node1 = PatternThatNode()
        node2 = PatternThatNode()

        with self.assertRaises(ParserException) as raised:
            node1.can_add(node2)
        self.assertEqual(str(raised.exception), "Cannot add that node to that node")

    def test_to_xml(self):
        node1 = PatternThatNode()
        self.assertEqual('<that></that>\n', node1.to_xml(self._client_context))
        self.assertEqual('<that userid="*"></that>\n', node1.to_xml(self._client_context, include_user=True))

        node2 = PatternThatNode(userid="testid")
        self.assertEqual('<that></that>\n', node2.to_xml(self._client_context))
        self.assertEqual('<that userid="testid"></that>\n', node2.to_xml(self._client_context, include_user=True))

    def test_to_string(self):
        node1 = PatternThatNode()
        self.assertEqual(node1.to_string(verbose=False), "THAT")
        self.assertEqual(node1.to_string(verbose=True), "THAT [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)]")

        node2 = PatternThatNode(userid="testid")
        self.assertEqual(node2.to_string(verbose=False), "THAT")
        self.assertEqual(node2.to_string(verbose=True), "THAT [testid] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)]")

    def test_equivalent(self):
        node1 = PatternThatNode()
        node2 = PatternThatNode()
        node3 = PatternTopicNode()
        node4 = PatternThatNode(userid="testid")

        self.assertTrue(node1.equivalent(node2))
        self.assertFalse(node1.equivalent(node3))
        self.assertFalse(node1.equivalent(node4))

    def test_consume_search_time_exceeded(self):
        node = PatternThatNode()
        self.assertIsNotNone(node)

        match_context = MatchContext(max_search_depth=100, max_search_timeout=0)
        words = Sentence(self._client_context)

        result = node.consume(self._client_context, match_context, words, 0, Match.WORD, 1, parent=False)
        self.assertIsNone(result)

    def test_consume_search_depth_exceeded(self):
        node = PatternThatNode()
        self.assertIsNotNone(node)

        match_context = MatchContext(max_search_depth=0, max_search_timeout=100)
        words = Sentence(self._client_context)

        result = node.consume(self._client_context, match_context, words, 0, Match.WORD, 1, parent=False)
        self.assertIsNone(result)


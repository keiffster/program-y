from test.parser.pattern.base import PatternTestBaseClass

from programy.parser.exceptions import ParserException
from programy.parser.pattern.nodes.zeroormore import PatternZeroOrMoreWildCardNode

class PatternZeroOrMoreWildCardNodeTests(PatternTestBaseClass):

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

        self.assertEqual(node.wildcard, "#")
        self.assertTrue(node.equivalent(PatternZeroOrMoreWildCardNode("#")))
        self.assertEqual(node.to_string(), "ZEROORMORE [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] wildcard=[#]")

    def test_arrow(self):
        node = PatternZeroOrMoreWildCardNode("^")
        self.assertIsNotNone(node)

        self.assertEqual(node.wildcard, "^")
        self.assertTrue(node.equivalent(PatternZeroOrMoreWildCardNode("^")))
        self.assertEqual(node.to_string(), "ZEROORMORE [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] wildcard=[^]")


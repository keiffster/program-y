from test.parser.pattern.test_nodes.base import PatternTestBaseClass
from programy.parser.pattern.nodes import *

from programy.parser.exceptions import ParserException
from programy.parser.pattern.nodes.zeroormore import PatternZeroOrMoreWildCardNode

class PatternZeroOrMoreWildCardNodeTests(PatternTestBaseClass):

    def test_invalid_wildcard(self):
        with self.assertRaises(ParserException) as raised:
            node = PatternZeroOrMoreWildCardNode("X")
            self.assertIsNone(node)

    def test_init(self):
        node = PatternZeroOrMoreWildCardNode("#")

        self.assertFalse(node.is_root())
        self.assertFalse(node.is_priority())
        self.assertTrue(node.is_wildcard())
        self.assertTrue(node.is_zero_or_more())
        self.assertFalse(node.is_one_or_more())
        self.assertIsNotNone(node.children)
        self.assertFalse(node.has_children())

        self.assertEqual(node.wildcard, "#")

        self.assertTrue(node.equivalent(PatternZeroOrMoreWildCardNode("#")))
        self.assertFalse(node.is_root())
        self.assertEqual(node.to_string(), "ZEROORMORE [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] wildcard=[#]")

        node = PatternZeroOrMoreWildCardNode("^")
        self.assertIsNotNone(node)

        self.assertEqual(node.wildcard, "^")

        self.assertTrue(node.equivalent(PatternZeroOrMoreWildCardNode("^")))
        self.assertFalse(node.is_root())
        self.assertEqual(node.to_string(), "ZEROORMORE [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] wildcard=[^]")


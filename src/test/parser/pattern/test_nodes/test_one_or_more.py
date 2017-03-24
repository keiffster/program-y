from programy.parser.exceptions import ParserException

from test.parser.pattern.test_nodes.base import PatternTestBaseClass
from programy.parser.pattern.nodes.oneormore import PatternOneOrMoreWildCardNode

class PatternOneOrMoreWildCardNodeTests(PatternTestBaseClass):

    def test_invalid_wildcard(self):
        with self.assertRaises(ParserException) as raised:
            node = PatternOneOrMoreWildCardNode("X")
            self.assertIsNone(node)

    def test_init(self):
        node = PatternOneOrMoreWildCardNode("*")
        self.assertIsNotNone(node)

        self.assertFalse(node.is_root())
        self.assertFalse(node.is_priority())
        self.assertTrue(node.is_wildcard())
        self.assertFalse(node.is_zero_or_more())
        self.assertTrue(node.is_one_or_more())

        self.assertIsNotNone(node.children)
        self.assertFalse(node.has_children())

        self.assertEqual(node.wildcard, "*")

        self.assertTrue(node.equivalent(PatternOneOrMoreWildCardNode("*")))
        self.assertFalse(node.is_root())
        self.assertEqual(node.to_string(), "ONEORMORE [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] wildcard=[*]")

        node = PatternOneOrMoreWildCardNode("_")
        self.assertIsNotNone(node)

        self.assertEqual(node.wildcard, "_")

        self.assertTrue(node.equivalent(PatternOneOrMoreWildCardNode("_")))
        self.assertFalse(node.is_root())
        self.assertEqual(node.to_string(), "ONEORMORE [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] wildcard=[_]")


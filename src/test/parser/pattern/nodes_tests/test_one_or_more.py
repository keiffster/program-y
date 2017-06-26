from test.parser.pattern.base import PatternTestBaseClass

from programy.parser.exceptions import ParserException
from programy.parser.pattern.nodes.oneormore import PatternOneOrMoreWildCardNode
from programy.dialog import Sentence

class PatternOneOrMoreWildCardNodeTests(PatternTestBaseClass):

    def test_invalid_wildcard(self):
        with self.assertRaises(ParserException) as raised:
            node = PatternOneOrMoreWildCardNode("X")
            self.assertIsNone(node)

    def test_star(self):
        node = PatternOneOrMoreWildCardNode("*")
        self.assertIsNotNone(node)

        self.assertFalse(node.is_root())
        self.assertFalse(node.is_priority())
        self.assertFalse(node.is_zero_or_more())
        self.assertTrue(node.is_one_or_more())
        self.assertFalse(node.is_set())
        self.assertFalse(node.is_bot())
        self.assertFalse(node.is_template())
        self.assertFalse(node.is_that())
        self.assertFalse(node.is_topic())
        self.assertTrue(node.is_wildcard())

        self.assertIsNotNone(node.children)
        self.assertFalse(node.has_children())

        self.assertEqual(node.wildcard, "*")

        sentence = Sentence("*")

        self.assertTrue(node.equivalent(PatternOneOrMoreWildCardNode("*")))
        result = node.equals(self.bot, "testid", sentence, 0)
        self.assertFalse(result.matched)
        self.assertEqual(node.to_string(), "ONEORMORE [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] wildcard=[*]")

    def test_underline(self):
        node = PatternOneOrMoreWildCardNode("_")
        self.assertIsNotNone(node)

        self.assertEqual(node.wildcard, "_")

        self.assertTrue(node.equivalent(PatternOneOrMoreWildCardNode("_")))
        self.assertEqual(node.to_string(), "ONEORMORE [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] wildcard=[_]")


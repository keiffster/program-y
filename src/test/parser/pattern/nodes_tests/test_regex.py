from test.parser.pattern.base import PatternTestBaseClass

from programy.parser.pattern.nodes.regex import PatternRegexNode

class PatternRegexNodeTests(PatternTestBaseClass):

    def test_init(self):

        node = PatternRegexNode("^LEGION$")
        self.assertIsNotNone(node)

        self.assertFalse(node.is_root())
        self.assertFalse(node.is_priority())
        self.assertFalse(node.is_wildcard())
        self.assertFalse(node.is_zero_or_more())
        self.assertFalse(node.is_one_or_more())
        self.assertFalse(node.is_set())
        self.assertFalse(node.is_bot())
        self.assertTrue(node.is_regex())
        self.assertFalse(node.is_template())
        self.assertFalse(node.is_that())
        self.assertFalse(node.is_topic())
        self.assertFalse(node.is_wildcard())

        self.assertIsNotNone(node.children)
        self.assertFalse(node.has_children())

        self.assertTrue(node.equivalent(PatternRegexNode("^LEGION$")))

        self.assertEqual(node.to_string(), "REGEX [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] pattern=[^LEGION$]")


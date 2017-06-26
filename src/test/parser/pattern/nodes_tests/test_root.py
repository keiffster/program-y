from test.parser.pattern.base import PatternTestBaseClass

from programy.parser.exceptions import ParserException

from programy.parser.pattern.nodes.word import PatternWordNode
from programy.parser.pattern.nodes.base import PatternNode
from programy.parser.pattern.nodes.root import PatternRootNode

class PatternRootNodeTests(PatternTestBaseClass):

    def test_init(self):
        node = PatternRootNode()
        self.assertIsNotNone(node)

        self.assertTrue(node.is_root())
        self.assertFalse(node.is_priority())
        self.assertFalse(node.is_wildcard())
        self.assertFalse(node.is_zero_or_more())
        self.assertFalse(node.is_one_or_more())
        self.assertFalse(node.is_set())
        self.assertFalse(node.is_bot())
        self.assertFalse(node.is_template())
        self.assertFalse(node.is_that())
        self.assertFalse(node.is_topic())
        self.assertFalse(node.is_wildcard())

        self.assertIsNotNone(node.children)
        self.assertFalse(node.has_children())

        self.assertTrue(node.equivalent(PatternRootNode()))
        self.assertEqual(node.to_string(), "ROOT [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)]")

        node.add_child(PatternNode())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.to_string(), "ROOT [P(0)^(0)#(0)C(1)_(0)*(0)To(0)Th(0)Te(0)]")

    def test_multiple_roots(self):
        node1 = PatternRootNode()
        node2 = PatternRootNode()

        with self.assertRaises(ParserException) as raised:
            node1.can_add(node2)
        self.assertTrue(str(raised.exception).startswith("Cannot add root node to existing root node"))

    def test_root_added_to_child(self):
        node1 = PatternWordNode("test")
        node2 = PatternRootNode()

        with self.assertRaises(ParserException) as raised:
            node1.can_add(node2)
        self.assertTrue(str(raised.exception).startswith("Cannot add root node to child node"))



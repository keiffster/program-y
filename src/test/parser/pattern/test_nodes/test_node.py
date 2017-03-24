from test.parser.pattern.test_nodes.base import PatternTestBaseClass

from programy.parser.pattern.nodes.base import PatternNode
from programy.parser.pattern.nodes.priority import PatternPriorityWordNode
from programy.parser.pattern.nodes.zeroormore import PatternZeroOrMoreWildCardNode

class PatternNodeTests(PatternTestBaseClass):

    def test_init(self):
        node = PatternNode()
        self.assertIsNotNone(node)
        self.assertFalse(node.is_root())
        self.assertFalse(node.is_priority())
        self.assertFalse(node.is_wildcard())
        self.assertFalse(node.is_zero_or_more())
        self.assertFalse(node.is_one_or_more())
        self.assertFalse(node.has_children())
        self.assertIsNotNone(node.children)

        self.assertFalse(node.equivalent(PatternNode()))
        self.assertEqual(node.to_string(), "NODE [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)]")

        node.add_child(PatternNode())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.to_string(), "NODE [P(0)^(0)#(0)C(1)_(0)*(0)To(0)Th(0)Te(0)]")

    def test_add_child(self):

        node = PatternNode()

        priority_word1 = PatternPriorityWordNode("pword")
        priority_word2 = PatternPriorityWordNode("pword")
        node.add_child(priority_word1)
        new_node = node.add_child(priority_word2)
        self.assertEqual(new_node, priority_word1)

        arrow_node1 = PatternZeroOrMoreWildCardNode("^")
        arrow_node2 = PatternZeroOrMoreWildCardNode("^")
        node.add_child(arrow_node1)
        new_node = node.add_child(arrow_node2)
        self.assertEqual(new_node, arrow_node1)



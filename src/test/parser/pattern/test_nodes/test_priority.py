from test.parser.pattern.test_nodes.base import PatternTestBaseClass

from programy.parser.pattern.nodes.word import PatternWordNode
from programy.parser.pattern.nodes.priority import PatternPriorityWordNode


class PatternPriorityWordNodeTests(PatternTestBaseClass):

    def test_init(self):
        node = PatternPriorityWordNode("test1")
        self.assertIsNotNone(node)

        self.assertFalse(node.is_root())
        self.assertTrue(node.is_priority())
        self.assertFalse(node.is_wildcard())
        self.assertFalse(node.is_zero_or_more())
        self.assertFalse(node.is_one_or_more())
        self.assertIsNotNone(node.children)
        self.assertFalse(node.has_children())

        self.assertTrue(node.equivalent(PatternPriorityWordNode("test1")))
        self.assertFalse(node.is_root())
        self.assertEqual(node.to_string(), "PWORD [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] word=[test1]")

        node.add_child(PatternWordNode("test2"))
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.to_string(), "PWORD [P(0)^(0)#(0)C(1)_(0)*(0)To(0)Th(0)Te(0)] word=[test1]")

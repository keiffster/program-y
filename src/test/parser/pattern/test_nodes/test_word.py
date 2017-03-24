from test.parser.pattern.test_nodes.base import PatternTestBaseClass
from programy.dialog import Sentence
from programy.parser.pattern.nodes import *

from programy.parser.exceptions import ParserException
from programy.parser.pattern.nodes.word import PatternWordNode

class PatternWordNodeTests(PatternTestBaseClass):

    def test_init(self):
        node = PatternWordNode("test1")

        self.assertFalse(node.is_root())
        self.assertFalse(node.is_priority())
        self.assertFalse(node.is_wildcard())
        self.assertFalse(node.is_zero_or_more())
        self.assertFalse(node.is_one_or_more())
        self.assertIsNotNone(node.children)
        self.assertFalse(node.has_children())

        self.assertTrue(node.equivalent(PatternWordNode("test1")))
        self.assertFalse(node.is_root())
        self.assertEqual(node.to_string(), "WORD [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] word=[test1]")

        node.add_child(PatternWordNode("test2"))
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.to_string(), "WORD [P(0)^(0)#(0)C(1)_(0)*(0)To(0)Th(0)Te(0)] word=[test1]")

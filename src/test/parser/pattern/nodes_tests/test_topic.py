from test.parser.pattern.base import PatternTestBaseClass

from programy.parser.exceptions import ParserException
from programy.parser.pattern.nodes.topic import PatternTopicNode
from programy.parser.pattern.nodes.root import PatternRootNode

class PatternTopicNodeTests(PatternTestBaseClass):

    def test_init(self):
        node = PatternTopicNode()
        self.assertIsNotNone(node)

        self.assertFalse(node.is_root())
        self.assertFalse(node.is_priority())
        self.assertFalse(node.is_wildcard())
        self.assertFalse(node.is_zero_or_more())
        self.assertFalse(node.is_one_or_more())
        self.assertFalse(node.is_set())
        self.assertFalse(node.is_bot())
        self.assertFalse(node.is_template())
        self.assertFalse(node.is_that())
        self.assertTrue(node.is_topic())
        self.assertFalse(node.is_wildcard())

        self.assertIsNotNone(node.children)
        self.assertFalse(node.has_children())

        self.assertTrue(node.equivalent(PatternTopicNode()))
        self.assertEqual(node.to_string(), "TOPIC [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)]")

    def test_topic_to_root(self):
        node1 = PatternRootNode()
        node2 = PatternTopicNode()

        with self.assertRaises(ParserException) as raised:
            node1.can_add(node2)
        self.assertEqual(str(raised.exception), "Cannot add topic node to root node")

    def test_multiple_topics(self):
        node1 = PatternTopicNode()
        node2 = PatternTopicNode()

        with self.assertRaises(ParserException) as raised:
            node1.can_add(node2)
        self.assertEqual(str(raised.exception), "Cannot add topic node to topic node")

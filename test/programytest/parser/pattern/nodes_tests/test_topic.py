from programytest.parser.base import ParserTestsBaseClass

from programy.parser.exceptions import ParserException
from programy.parser.pattern.nodes.that import PatternThatNode
from programy.parser.pattern.nodes.topic import PatternTopicNode
from programy.parser.pattern.nodes.root import PatternRootNode

class PatternTopicNodeTests(ParserTestsBaseClass):

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
        self.assertEqual(node.to_string(), "TOPIC [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)]")
        self.assertEqual(node.to_string(verbose=False), "TOPIC")

        self.assertEqual("<topic></topic>\n", node.to_xml(self._client_context))

    def test_root_to_topic(self):
        node1 = PatternTopicNode()
        node2 = PatternRootNode()

        with self.assertRaises(ParserException) as raised:
            node1.can_add(node2)
        self.assertEqual(str(raised.exception), "Cannot add root node to topic node")

    def test_topic_to_topic(self):
        node1 = PatternTopicNode()
        node2 = PatternTopicNode()

        with self.assertRaises(ParserException) as raised:
            node1.can_add(node2)
        self.assertEqual(str(raised.exception), "Cannot add topic node to topic node")

    def test_that_to_topic(self):
        node1 = PatternTopicNode()
        node2 = PatternThatNode()

        with self.assertRaises(ParserException) as raised:
            node1.can_add(node2)
        self.assertEqual(str(raised.exception), "Cannot add that node to topic node")

    def test_to_xml(self):
        node1 = PatternTopicNode()
        self.assertEqual('<topic></topic>\n', node1.to_xml(self._client_context))
        self.assertEqual('<topic userid="*"></topic>\n', node1.to_xml(self._client_context, include_user=True))

        node2 = PatternTopicNode(userid="testid")
        self.assertEqual('<topic></topic>\n', node2.to_xml(self._client_context))
        self.assertEqual('<topic userid="testid"></topic>\n', node2.to_xml(self._client_context, include_user=True))

    def test_to_string(self):
        node1 = PatternTopicNode()
        self.assertEqual(node1.to_string(verbose=False), "TOPIC")
        self.assertEqual(node1.to_string(verbose=True), "TOPIC [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)]")

        node2 = PatternTopicNode(userid="testid")
        self.assertEqual(node2.to_string(verbose=False), "TOPIC")
        self.assertEqual(node2.to_string(verbose=True), "TOPIC [testid] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)]")

    def test_equivalent(self):
        node1 = PatternTopicNode()
        node2 = PatternTopicNode()
        node3 = PatternThatNode()
        node4 = PatternTopicNode(userid="testid")

        self.assertTrue(node1.equivalent(node2))
        self.assertFalse(node1.equivalent(node3))
        self.assertFalse(node1.equivalent(node4))

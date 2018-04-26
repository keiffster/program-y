from programytest.parser.base import ParserTestsBaseClass

from programy.parser.exceptions import ParserException
from programy.parser.template.nodes.base import TemplateNode
from programy.parser.pattern.nodes.template import PatternTemplateNode
from programy.parser.pattern.nodes.root import PatternRootNode
from programy.parser.pattern.nodes.topic import PatternTopicNode
from programy.parser.pattern.nodes.that import PatternThatNode


class PatternTemplateNodeTests(ParserTestsBaseClass):

    def test_init(self):

        node = PatternTemplateNode(TemplateNode())
        self.assertIsNotNone(node)

        self.assertFalse(node.is_root())
        self.assertFalse(node.is_priority())
        self.assertFalse(node.is_wildcard())
        self.assertFalse(node.is_zero_or_more())
        self.assertFalse(node.is_one_or_more())
        self.assertFalse(node.is_set())
        self.assertFalse(node.is_bot())
        self.assertTrue(node.is_template())
        self.assertFalse(node.is_that())
        self.assertFalse(node.is_topic())
        self.assertFalse(node.is_wildcard())

        self.assertIsNotNone(node.children)
        self.assertFalse(node.has_children())

        self.assertTrue(node.equivalent(PatternTemplateNode(TemplateNode())))
        self.assertEqual(node.to_string(), "PTEMPLATE [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(1)]")
        self.assertEqual(node.to_string(verbose=False), "PTEMPLATE")
        self.assertEqual('<template></template>\n', node.to_xml(self._client_context))

        self.assertFalse(node.equivalent(PatternTopicNode()))

    def test_to_xml(self):
        node1 = PatternTemplateNode(TemplateNode())
        self.assertEqual('<template></template>\n', node1.to_xml(self._client_context))
        self.assertEqual('<template userid="*"></template>\n', node1.to_xml(self._client_context, include_user=True))

        node2 = PatternTemplateNode(TemplateNode(), userid="testid")
        self.assertEqual('<template></template>\n', node2.to_xml(self._client_context))
        self.assertEqual('<template userid="testid"></template>\n', node2.to_xml(self._client_context, include_user=True))

    def test_to_string(self):
        node1 = PatternTemplateNode(TemplateNode())
        self.assertEqual(node1.to_string(verbose=False), "PTEMPLATE")
        self.assertEqual(node1.to_string(), "PTEMPLATE [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(1)]")

        node2 = PatternTemplateNode(TemplateNode(), userid="testid")
        self.assertEqual(node2.to_string(verbose=False), "PTEMPLATE")
        self.assertEqual(node2.to_string(), "PTEMPLATE [testid] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(1)]")

    def test_equivalent(self):
        node1 = PatternTemplateNode(TemplateNode())
        node2 = PatternTemplateNode(TemplateNode())
        node3 = PatternTemplateNode(TemplateNode(), userid="testid")

        self.assertTrue(node1.equivalent(node2))
        self.assertFalse(node1.equivalent(node3))

    def test_root_to_template(self):
        node1 = PatternTemplateNode(TemplateNode())
        node2 = PatternRootNode()

        with self.assertRaises(ParserException) as raised:
            node1.can_add(node2)
        self.assertEqual(str(raised.exception), "Cannot add root node to template node")

    def test_template_to_template(self):
        node1 = PatternTemplateNode(TemplateNode())
        node2 = PatternTemplateNode(TemplateNode())

        with self.assertRaises(ParserException) as raised:
            node1.can_add(node2)
        self.assertEqual(str(raised.exception), "Cannot add template node to template node")

    def test_topic_to_template(self):
        node1 = PatternTemplateNode(TemplateNode())
        node2 = PatternTopicNode()

        with self.assertRaises(ParserException) as raised:
            node1.can_add(node2)
        self.assertEqual(str(raised.exception), "Cannot add topic node to template node")

    def test_that_to_template(self):
        node1 = PatternTemplateNode(TemplateNode())
        node2 = PatternThatNode()

        with self.assertRaises(ParserException) as raised:
            node1.can_add(node2)
        self.assertEqual(str(raised.exception), "Cannot add that node to template node")

    def test_multiple_templates(self):
        node1 = PatternTemplateNode(TemplateNode())
        node2 = PatternTemplateNode(TemplateNode())

        with self.assertRaises(ParserException) as raised:
            node1.can_add(node2)
        self.assertEqual(str(raised.exception), "Cannot add template node to template node")



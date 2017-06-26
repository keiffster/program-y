from test.parser.pattern.base import PatternTestBaseClass

from programy.parser.exceptions import ParserException
from programy.parser.template.nodes.base import TemplateNode
from programy.parser.pattern.nodes.template import PatternTemplateNode
from programy.parser.pattern.nodes.root import PatternRootNode


class PatternTemplateNodeTests(PatternTestBaseClass):

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
        self.assertEqual(node.to_string(), "PTEMPLATE [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(1)] ")

    def test_template_to_root(self):
        node1 = PatternRootNode()
        node2 = PatternTemplateNode(TemplateNode())

        with self.assertRaises(ParserException) as raised:
            node1.can_add(node2)
        self.assertEqual(str(raised.exception), "Cannot add template node to root node")

    def test_multiple_templates(self):
        node1 = PatternTemplateNode(TemplateNode())
        node2 = PatternTemplateNode(TemplateNode())

        with self.assertRaises(ParserException) as raised:
            node1.can_add(node2)
        self.assertEqual(str(raised.exception), "Cannot add template node to template node")



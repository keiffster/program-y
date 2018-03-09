from programytest.parser.base import ParserTestsBaseClass

from programy.parser.pattern.nodes.regex import PatternRegexNode
from programy.parser.exceptions import ParserException


class PatternRegexNodeTests(ParserTestsBaseClass):

    def test_init_with_text(self):
        node = PatternRegexNode({}, "^LEGION$")
        self.assertIsNotNone(node)
        self.assertIsNone(node._pattern_template)
        self.assertEqual("^LEGION$", node._pattern_text)

    def test_init_with_pattern_attrib(self):
        node = PatternRegexNode({"pattern": "^LEGION$"}, "")
        self.assertIsNotNone(node)
        self.assertIsNone(node._pattern_template)
        self.assertEqual("^LEGION$", node._pattern_text)

    def test_init_with_template_attrib(self):
        node = PatternRegexNode({"template": "PhoneNumber"}, "")
        self.assertIsNotNone(node)
        self.assertIsNone(node._pattern_text)
        self.assertEqual("PhoneNumber", node._pattern_template)

    def test_init_with_invalid_attribs(self):
        with self.assertRaises(ParserException) as raised:
            node = PatternRegexNode({"unknwon": "test1"}, "")
        self.assertEqual(str(raised.exception), "Invalid regex node, neither pattern or template specified as attribute or text")

    def test_init_with_nothing(self):
        with self.assertRaises(ParserException) as raised:
            node = PatternRegexNode({}, "")
        self.assertEqual(str(raised.exception), "Invalid regex node, neither pattern or template specified as attribute or text")

    def test_init_pattern(self):

        node = PatternRegexNode({}, "^LEGION$")
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

        self.assertTrue(node.equivalent(PatternRegexNode({}, "^LEGION$")))

        self.assertEqual(node.to_string(), "REGEX [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] pattern=[^LEGION$]")
        self.assertEqual('<regex pattern="^LEGION$"></regex>\n', node.to_xml(self._client_context))

    def test_init_template(self):

        node = PatternRegexNode({"template": "LEGION"}, "")
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

        self.assertTrue(node.equivalent(PatternRegexNode({"template": "LEGION"}, "")))

        self.assertEqual(node.to_string(), "REGEX [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] template=[LEGION]")
        self.assertEqual('<regex template="LEGION"></regex>\n', node.to_xml(self._client_context))

import re

from programy.dialog.sentence import Sentence
from programy.parser.exceptions import ParserException
from programy.parser.pattern.nodes.regex import PatternRegexNode
from programy.parser.pattern.nodes.word import PatternWordNode
from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.word import TemplateWordNode
from programytest.parser.base import ParserTestsBaseClass


class PatternRegexNodeTests(ParserTestsBaseClass):

    def test_init_with_text(self):
        node = PatternRegexNode({}, "^LEGION$")
        self.assertIsNotNone(node)
        self.assertIsNone(node.pattern_template)
        self.assertEqual("^LEGION$", node.pattern_text)

    def test_init_with_pattern_attrib(self):
        node = PatternRegexNode({"pattern": "^LEGION$"}, "")
        self.assertIsNotNone(node)
        self.assertIsNone(node.pattern_template)
        self.assertEqual("^LEGION$", node.pattern_text)

    def test_init_with_template_attrib(self):
        node = PatternRegexNode({"template": "PhoneNumber"}, "")
        self.assertIsNotNone(node)
        self.assertIsNone(node.pattern_text)
        self.assertEqual("PhoneNumber", node.pattern_template)

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

    def test_to_xml_pattern(self):
        node1 = PatternRegexNode({}, "^LEGION$")
        self.assertEqual('<regex pattern="^LEGION$"></regex>\n', node1.to_xml(self._client_context, include_user=False))
        self.assertEqual('<regex userid="*" pattern="^LEGION$"></regex>\n', node1.to_xml(self._client_context, include_user=True))

        node2 = PatternRegexNode({}, "^LEGION$", userid="testid")
        self.assertEqual('<regex pattern="^LEGION$"></regex>\n', node2.to_xml(self._client_context, include_user=False))
        self.assertEqual('<regex userid="testid" pattern="^LEGION$"></regex>\n', node2.to_xml(self._client_context, include_user=True))

    def test_to_xml_template(self):
        node1 = PatternRegexNode({"template": "LEGION"}, "")
        self.assertEqual('<regex template="LEGION"></regex>\n', node1.to_xml(self._client_context, include_user=False))
        self.assertEqual('<regex userid="*" template="LEGION"></regex>\n', node1.to_xml(self._client_context, include_user=True))

        node2 = PatternRegexNode({"template": "LEGION"}, "", userid="testid")
        self.assertEqual('<regex template="LEGION"></regex>\n', node2.to_xml(self._client_context, include_user=False))
        self.assertEqual('<regex userid="testid" template="LEGION"></regex>\n', node2.to_xml(self._client_context, include_user=True))

    def test_to_string_pattern(self):
        node1 = PatternRegexNode({}, "^LEGION$")
        self.assertEqual(node1.to_string(verbose=False), "REGEX pattern=[^LEGION$]")
        self.assertEqual(node1.to_string(verbose=True), "REGEX [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] pattern=[^LEGION$]")

        node2 = PatternRegexNode({}, "^LEGION$", userid="testid")
        self.assertEqual(node2.to_string(verbose=False), "REGEX pattern=[^LEGION$]")
        self.assertEqual(node2.to_string(verbose=True), "REGEX [testid] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] pattern=[^LEGION$]")

    def test_to_string_template(self):
        node1 = PatternRegexNode({"template": "LEGION"}, "")
        self.assertEqual(node1.to_string(verbose=False), "REGEX template=[LEGION]")
        self.assertEqual(node1.to_string(verbose=True), "REGEX [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] template=[LEGION]")

        node2 = PatternRegexNode({"template": "LEGION"}, "", userid="testid")
        self.assertEqual(node2.to_string(verbose=False), "REGEX template=[LEGION]")
        self.assertEqual(node2.to_string(verbose=True), "REGEX [testid] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] template=[LEGION]")

    def test_equivalent_pattern(self):
        node1 = PatternRegexNode({}, "^LEGION$")
        node2 = PatternRegexNode({}, "^LEGION$")
        node3 = PatternRegexNode({}, "^LEGION$", userid="testuser")

        self.assertTrue(node1.equivalent(node2))
        self.assertFalse(node1.equivalent(node3))

    def test_equivalent_template(self):
        node1 = PatternRegexNode({"template": "LEGION"}, "")
        node2 = PatternRegexNode({"template": "LEGION"}, "")
        node3 = PatternRegexNode({"template": "LEGION"}, "", userid="testuser")

        self.assertTrue(node1.equivalent(node2))
        self.assertFalse(node1.equivalent(node3))

    def test_equals_pattern(self):
        node1 = PatternRegexNode({}, "^LEGION$")
        node2 = PatternRegexNode({}, "^LEGION$", userid="testid")
        node3 = PatternRegexNode({}, "^LEGION$", userid="testid2")

        match1 = node1.equals(self._client_context, Sentence(self._client_context, 'LEGION'), 0)
        self.assertIsNotNone(match1)
        self.assertTrue(match1.matched)

        match2 = node2.equals(self._client_context, Sentence(self._client_context, 'LEGION'), 0)
        self.assertIsNotNone(match2)
        self.assertTrue(match2.matched)

        match3 = node3.equals(self._client_context, Sentence(self._client_context, 'LEGION'), 0)
        self.assertIsNotNone(match3)
        self.assertFalse(match3.matched)

    def test_equals_template(self):
        self._client_context.brain.regex_templates.add_regex("LEGION", re.compile("^LEGION$", re.IGNORECASE))

        node1 = PatternRegexNode({"template": "LEGION"}, "")
        node2 = PatternRegexNode({"template": "LEGION"}, "", userid="testid")
        node3 = PatternRegexNode({"template": "LEGION"}, "", userid="testid2")

        match1 = node1.equals(self._client_context, Sentence(self._client_context, 'LEGION'), 0)
        self.assertIsNotNone(match1)
        self.assertTrue(match1.matched)

        match2 = node2.equals(self._client_context, Sentence(self._client_context, 'LEGION'), 0)
        self.assertIsNotNone(match2)
        self.assertTrue(match2.matched)

        match3 = node3.equals(self._client_context, Sentence(self._client_context, 'LEGION'), 0)
        self.assertIsNotNone(match3)
        self.assertFalse(match3.matched)

    def test_not_equals_template(self):
        self._client_context.brain.regex_templates.add_regex("LEGION", re.compile("^LEGION$", re.IGNORECASE))

        node1 = PatternRegexNode({"template": "OTHER"}, "")
        match = node1.equals(self._client_context, Sentence(self._client_context, 'LEGION'), 0)
        self.assertIsNotNone(match)
        self.assertFalse(match.matched)

    def test_equivalent_mixed(self):
        node1 = PatternRegexNode({}, "^LEGION$")
        node2 = PatternRegexNode({}, "^LEGION$", userid="testid")
        node3 = PatternRegexNode({}, "^LEGION$", userid="testid2")

        self._client_context.brain.regex_templates.add_regex("LEGION", re.compile("^LEGION$", re.IGNORECASE))

        node4 = PatternRegexNode({"template": "LEGION"}, "")
        node5 = PatternRegexNode({"template": "LEGION"}, "", userid="testid")
        node6 = PatternRegexNode({"template": "LEGION"}, "", userid="testid2")

        self.assertFalse(node1.equivalent(node4))
        self.assertFalse(node2.equivalent(node5))
        self.assertFalse(node3.equivalent(node6))

    def test_equivalent_none_regex(self):
        node1 = PatternRegexNode({}, "^LEGION$")
        node2 = PatternWordNode("test")

        self.assertFalse(node1.equivalent(node2))

    def test_equivalent_at_template_level(self):
        node1 = PatternRegexNode({}, "^LEGION$")
        template1 = TemplateNode()
        template1.append(TemplateWordNode("test"))
        node1.add_template(template1)

        node2 = PatternRegexNode({}, "^LEGION$")
        template2 = TemplateNode()
        template2.append(TemplateWordNode("test"))
        node1.add_template(template2)

        self.assertTrue(node1.equivalent(node2))

    def test_not_at_equivalent_at_template_level(self):
        node1 = PatternRegexNode({}, "^LEGION$")
        template1 = TemplateNode()
        template1.append(TemplateWordNode("test1"))
        node1.add_template(template1)

        node2 = PatternRegexNode({}, "^LEGION$")
        template2 = TemplateNode()
        template2.append(TemplateWordNode("test2"))
        node1.add_template(template2)

        self.assertTrue(node1.equivalent(node2))

    def test_equivalent_at_pattern_template_level(self):
        node1 = PatternRegexNode({"template": ".*"}, "^LEGION$")
        node2 = PatternRegexNode({"template": ".*"}, "^LEGION$")
        self.assertTrue(node1.equivalent(node2))

    def test_not_equivalent_at_pattern_template_level(self):
        node1 = PatternRegexNode({"template": ".*"}, "^LEGION$")
        node2 = PatternRegexNode({"template": "[A-Z]"}, "^LEGION$")
        self.assertFalse(node1.equivalent(node2))

    def test_equivalent_at_pattern_template_missing_lhs(self):
        node1 = PatternRegexNode({}, "^LEGION$")
        node2 = PatternRegexNode({"template": "[A-Z]"}, "^LEGION$")
        self.assertFalse(node1.equivalent(node2))

    def test_equivalent_at_pattern_template_missing_rhs(self):
        node1 = PatternRegexNode({"template": "[A-Z]"}, "^LEGION$")
        node2 = PatternRegexNode({}, "^LEGION$")
        self.assertFalse(node1.equivalent(node2))

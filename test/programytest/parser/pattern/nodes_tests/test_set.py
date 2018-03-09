from programytest.parser.base import ParserTestsBaseClass

from programy.parser.pattern.nodes.set import PatternSetNode
from programy.dialog.dialog import Sentence
from programy.mappings.sets import SetLoader
from programy.parser.exceptions import ParserException


class PatternSetNodeTests(ParserTestsBaseClass):

    def test_init_with_text(self):
        node = PatternSetNode({}, "test1")
        self.assertIsNotNone(node)
        self.assertEqual("TEST1", node.set_name)

    def test_init_with_attribs(self):
        node = PatternSetNode({"name": "test1"}, "")
        self.assertIsNotNone(node)
        self.assertEqual("TEST1", node.set_name)

    def test_init_with_invalid_attribs(self):
        with self.assertRaises(ParserException) as raised:
            node = PatternSetNode({"unknwon": "test1"}, "")
        self.assertEqual(str(raised.exception), "Invalid set node, no name specified as attribute or text")

    def test_init_with_nothing(self):
        with self.assertRaises(ParserException) as raised:
            node = PatternSetNode({}, "")
        self.assertEqual(str(raised.exception), "Invalid set node, no name specified as attribute or text")

    def test_init(self):
        loader = SetLoader()

        self._client_context.brain._sets_collection._sets["TEST1"] = loader.load_from_text("""
            VALUE1
            VALUE2
            VALUE3
            VALUE4
        """)

        node = PatternSetNode([], "test1")
        self.assertIsNotNone(node)

        self.assertFalse(node.is_root())
        self.assertFalse(node.is_priority())
        self.assertFalse(node.is_wildcard())
        self.assertFalse(node.is_zero_or_more())
        self.assertFalse(node.is_one_or_more())
        self.assertTrue(node.is_set())
        self.assertFalse(node.is_bot())
        self.assertFalse(node.is_template())
        self.assertFalse(node.is_that())
        self.assertFalse(node.is_topic())
        self.assertFalse(node.is_wildcard())

        self.assertIsNotNone(node.children)
        self.assertFalse(node.has_children())

        sentence = Sentence(self._client_context.brain.tokenizer, "VALUE1 VALUE2 VALUE3 VALUE4")

        self.assertTrue(node.equivalent(PatternSetNode([], "TEST1")))
        result = node.equals(self._client_context, sentence, 0)
        self.assertTrue(result.matched)
        result = node.equals(self._client_context, sentence, 1)
        self.assertTrue(result.matched)
        result = node.equals(self._client_context, sentence, 2)
        self.assertTrue(result.matched)
        result = node.equals(self._client_context, sentence, 3)
        self.assertTrue(result.matched)
        self.assertEqual(node.to_string(), "SET [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] name=[TEST1]")
        self.assertEqual('<set name="TEST1">\n</set>', node.to_xml(self._client_context))

    def test_multi_word_set(self):
        loader = SetLoader()

        self._client_context.brain._sets_collection._sets["TEST1"] = loader.load_from_text("""
            Red
            Red Amber
            Red Brown
        """)

        node = PatternSetNode([], "test1")
        self.assertIsNotNone(node)

        self.assertFalse(node.is_root())
        self.assertFalse(node.is_priority())
        self.assertFalse(node.is_wildcard())
        self.assertFalse(node.is_zero_or_more())
        self.assertFalse(node.is_one_or_more())
        self.assertTrue(node.is_set())
        self.assertFalse(node.is_bot())
        self.assertFalse(node.is_template())
        self.assertFalse(node.is_that())
        self.assertFalse(node.is_topic())
        self.assertFalse(node.is_wildcard())

        self.assertTrue(node.equivalent(PatternSetNode([], "TEST1")))
        self.assertIsNotNone(node.children)
        self.assertFalse(node.has_children())

        sentence = Sentence(self._client_context.brain.tokenizer, "RED Red BROWN red AMBER")

        result = node.equals(self._client_context, sentence, 0)
        self.assertTrue(result.matched)
        self.assertEquals(result.matched_phrase, "Red")
        self.assertEquals(result.word_no, 0)

        result = node.equals(self._client_context, sentence, result.word_no+1)
        self.assertTrue(result.matched)
        self.assertEquals(result.matched_phrase, "Red Brown")

        result = node.equals(self._client_context, sentence, result.word_no+1)
        self.assertTrue(result.matched)
        self.assertEquals(result.matched_phrase, "Red Amber")

        self.assertEqual(node.to_string(), "SET [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] name=[TEST1]")
        self.assertEqual('<set name="TEST1">\n</set>', node.to_xml(self._client_context))

    def test_number(self):
        self._client_context.brain.dynamics.add_dynamic_set('number', "programy.dynamic.sets.numeric.IsNumeric", None)

        node = PatternSetNode([], "NUMBER")
        self.assertIsNotNone(node)

        sentence = Sentence(self._client_context.brain.tokenizer, "12 XY")

        result = node.equals(self._client_context, sentence, 0)
        self.assertTrue(result.matched)

        result = node.equals(self._client_context, sentence, result.word_no+1)
        self.assertFalse(result.matched)


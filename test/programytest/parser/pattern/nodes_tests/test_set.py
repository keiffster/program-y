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
        self.assertEqual(node.to_string(), "SET [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] name=[TEST1]")
        self.assertEqual('<set name="TEST1">\n</set>', node.to_xml(self._client_context))

    def test_multi_node_set(self):
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

        self.assertEqual(node.to_string(), "SET [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] name=[TEST1]")
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

    def test_to_xml_text(self):
        node1 = PatternSetNode({}, "test1")
        self.assertEqual('<set name="TEST1">\n</set>', node1.to_xml(self._client_context))
        self.assertEqual('<set userid="*" name="TEST1">\n</set>', node1.to_xml(self._client_context, include_user=True))

        node2 = PatternSetNode({}, "test1", userid="testid")
        self.assertEqual('<set name="TEST1">\n</set>', node2.to_xml(self._client_context))
        self.assertEqual('<set userid="testid" name="TEST1">\n</set>', node2.to_xml(self._client_context, include_user=True))

    def test_to_xml_attribs(self):
        node1 = PatternSetNode({"name": "test1"}, "")
        self.assertEqual('<set name="TEST1">\n</set>', node1.to_xml(self._client_context))
        self.assertEqual('<set userid="*" name="TEST1">\n</set>', node1.to_xml(self._client_context, include_user=True))

        node2 = PatternSetNode({"name": "test1"}, "", userid="testid")
        self.assertEqual('<set name="TEST1">\n</set>', node2.to_xml(self._client_context))
        self.assertEqual('<set userid="testid" name="TEST1">\n</set>', node2.to_xml(self._client_context, include_user=True))

    def test_to_string_text(self):
        node1 = PatternSetNode({}, "test1")
        self.assertEqual('SET name=[TEST1]', node1.to_string(verbose=False))
        self.assertEqual('SET [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] name=[TEST1]', node1.to_string(verbose=True))

        node2 = PatternSetNode({}, "test1", userid="testid")
        self.assertEqual('SET name=[TEST1]', node2.to_string(verbose=False))
        self.assertEqual('SET [testid] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] name=[TEST1]', node2.to_string(verbose=True))
        pass

    def test_to_string_attribs(self):
        node1 = PatternSetNode({"name": "test1"}, "")
        self.assertEqual('SET name=[TEST1]', node1.to_string(verbose=False))
        self.assertEqual('SET [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] name=[TEST1]', node1.to_string(verbose=True))

        node2 = PatternSetNode({"name": "test1"}, "", userid="testid")
        self.assertEqual('SET name=[TEST1]', node2.to_string(verbose=False))
        self.assertEqual('SET [testid] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] name=[TEST1]', node2.to_string(verbose=True))
        pass

    def test_equivalent_text(self):
        node1 = PatternSetNode({}, "test1")
        node2 = PatternSetNode({}, "test1")
        node3 = PatternSetNode({}, "test1", userid="testid")

        self.assertTrue(node1.equivalent(node2))
        self.assertFalse(node1.equivalent(node3))

    def test_equivalent_attribs(self):
        node1 = PatternSetNode({"name": "test1"}, "")
        node2 = PatternSetNode({"name": "test1"}, "")
        node3 = PatternSetNode({"name": "test1"}, "", userid="testid")

        self.assertTrue(node1.equivalent(node2))
        self.assertFalse(node1.equivalent(node3))

    def test_equals_text(self):
        loader = SetLoader()

        self._client_context.brain._sets_collection._sets["TEST1"] = loader.load_from_text("""
                    VALUE1
                    VALUE2
                    VALUE3
                    VALUE4
                """)

        node1 = PatternSetNode({}, "test1")
        node2 = PatternSetNode({}, "test1", userid="testid")
        node3 = PatternSetNode({}, "test1", userid="testid2")

        match1 = node1.equals(self._client_context, Sentence(self._client_context.brain.tokenizer, 'VALUE1'), 0)
        self.assertIsNotNone(match1)
        self.assertTrue(match1.matched)

        match2 = node2.equals(self._client_context, Sentence(self._client_context.brain.tokenizer, 'VALUE1'), 0)
        self.assertIsNotNone(match2)
        self.assertTrue(match2.matched)

        match3 = node3.equals(self._client_context, Sentence(self._client_context.brain.tokenizer, 'VALUE1'), 0)
        self.assertIsNotNone(match3)
        self.assertFalse(match3.matched)

    def test_equals_attribs(self):
        loader = SetLoader()

        self._client_context.brain._sets_collection._sets["TEST1"] = loader.load_from_text("""
                    VALUE1
                    VALUE2
                    VALUE3
                    VALUE4
                """)

        node1 = PatternSetNode({"name": "test1"}, "")
        node2 = PatternSetNode({"name": "test1"}, "", userid="testid")
        node3 = PatternSetNode({"name": "test1"}, "", userid="testid2")

        match1 = node1.equals(self._client_context, Sentence(self._client_context.brain.tokenizer, 'VALUE1'), 0)
        self.assertIsNotNone(match1)
        self.assertTrue(match1.matched)

        match2 = node2.equals(self._client_context, Sentence(self._client_context.brain.tokenizer, 'VALUE1'), 0)
        self.assertIsNotNone(match2)
        self.assertTrue(match2.matched)

        match3 = node3.equals(self._client_context, Sentence(self._client_context.brain.tokenizer, 'VALUE1'), 0)
        self.assertIsNotNone(match3)
        self.assertFalse(match3.matched)

    def test_equals_mixed(self):
        loader = SetLoader()

        self._client_context.brain._sets_collection._sets["TEST1"] = loader.load_from_text("""
                    VALUE1
                    VALUE2
                    VALUE3
                    VALUE4
                """)

        node1 = PatternSetNode({}, "test1")
        node2 = PatternSetNode({}, "test1", userid="testid")
        node3 = PatternSetNode({}, "test1", userid="testid2")

        node4 = PatternSetNode({"name": "test1"}, "")
        node5 = PatternSetNode({"name": "test1"}, "", userid="testid")
        node6 = PatternSetNode({"name": "test1"}, "", userid="testid2")

        self.assertTrue(node1.equivalent(node4))
        self.assertTrue(node2.equivalent(node5))
        self.assertTrue(node3.equivalent(node6))

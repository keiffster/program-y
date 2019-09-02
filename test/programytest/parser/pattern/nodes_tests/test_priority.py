from programytest.parser.base import ParserTestsBaseClass

from programy.parser.pattern.nodes.word import PatternWordNode
from programy.parser.pattern.nodes.priority import PatternPriorityWordNode
from programy.dialog.sentence import Sentence


class PatternPriorityWordNodeTests(ParserTestsBaseClass):

    def test_init(self):
        node = PatternPriorityWordNode("test1")
        self.assertIsNotNone(node)

        self.assertFalse(node.is_root())
        self.assertTrue(node.is_priority())
        self.assertFalse(node.is_wildcard())
        self.assertFalse(node.is_zero_or_more())
        self.assertFalse(node.is_one_or_more())
        self.assertFalse(node.is_set())
        self.assertFalse(node.is_bot())
        self.assertFalse(node.is_template())
        self.assertFalse(node.is_that())
        self.assertFalse(node.is_topic())
        self.assertFalse(node.is_wildcard())

        self.assertIsNotNone(node.children)
        self.assertFalse(node.has_children())

        sentence = Sentence(self._client_context, "test1 test2")
        self.assertTrue(node.equivalent(PatternPriorityWordNode("test1")))
        result = node.equals(self._client_context, sentence, 0)
        self.assertTrue(result.matched)
        result = node.equals(self._client_context, sentence, 1)
        self.assertFalse(result.matched)
        self.assertEqual(node.to_string(), "PWORD [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] word=[test1]")
        self.assertEqual('<priority word="test1"></priority>\n', node.to_xml(self._client_context))

        node.add_child(PatternWordNode("test2"))
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.to_string(), "PWORD [*] [P(0)^(0)#(0)C(1)_(0)*(0)To(0)Th(0)Te(0)] word=[test1]")
        self.assertEqual('<priority word="test1"><word word="test2"></word>\n</priority>\n', node.to_xml(self._client_context))

    def test_to_xml(self):
        word1 = PatternPriorityWordNode("test1")
        self.assertEqual('<priority word="test1"></priority>\n', word1.to_xml(self._client_context))
        self.assertEqual('<priority userid="*" word="test1"></priority>\n', word1.to_xml(self._client_context, include_user=True))

        word2 = PatternPriorityWordNode("test2", userid="testid")
        self.assertEqual('<priority word="test2"></priority>\n', word2.to_xml(self._client_context))
        self.assertEqual('<priority userid="testid" word="test2"></priority>\n', word2.to_xml(self._client_context, include_user=True))

    def test_to_string(self):
        word1 = PatternPriorityWordNode("test1")
        self.assertEqual("PWORD [test1]", word1.to_string(verbose=False))
        self.assertEqual("PWORD [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] word=[test1]", word1.to_string(verbose=True))

        word2 = PatternPriorityWordNode("test2", "testid")
        self.assertEqual("PWORD [test2]", word2.to_string(verbose=False))
        self.assertEqual("PWORD [testid] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] word=[test2]", word2.to_string(verbose=True))

    def test_equivalent_userid(self):
        word1 = PatternPriorityWordNode("word")
        word2 = PatternPriorityWordNode("word")
        word3 = PatternPriorityWordNode("word", userid="testuser")

        self.assertTrue(word1.equivalent(word2))
        self.assertFalse(word1.equivalent(word3))

    def test_equals_userid(self):
        word1 = PatternPriorityWordNode("word")
        word2 = PatternPriorityWordNode("word", userid="testid")
        word3 = PatternPriorityWordNode("word", userid="testid2")

        match1 = word1.equals(self._client_context, Sentence(self._client_context, 'word'), 0)
        self.assertIsNotNone(match1)
        self.assertTrue(match1.matched)

        match2 = word2.equals(self._client_context, Sentence(self._client_context, 'word'), 0)
        self.assertIsNotNone(match2)
        self.assertTrue(match2.matched)

        match3 = word3.equals(self._client_context, Sentence(self._client_context, 'word'), 0)
        self.assertIsNotNone(match3)
        self.assertFalse(match3.matched)

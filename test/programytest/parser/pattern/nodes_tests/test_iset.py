from programytest.parser.base import ParserTestsBaseClass

from programy.parser.pattern.nodes.iset import PatternISetNode
from programy.dialog.sentence import Sentence
from programy.parser.exceptions import ParserException

class PatternSetNodeTests(ParserTestsBaseClass):

    def test_init_with_text(self):
        node = PatternISetNode({}, "test1, test2, test3")
        self.assertIsNotNone(node)
        self.assertEqual("TEST1", node.words[0])
        self.assertEqual("TEST2", node.words[1])
        self.assertEqual("TEST3", node.words[2])

    def test_init_with_attribs(self):
        node = PatternISetNode({"words": "test1, test2, test3"}, "")
        self.assertIsNotNone(node)
        self.assertEqual("TEST1", node.words[0])
        self.assertEqual("TEST2", node.words[1])
        self.assertEqual("TEST3", node.words[2])

    def test_init_with_invalid_attribs(self):
        with self.assertRaises(ParserException) as raised:
            node = PatternISetNode({"unknwon": "test1"}, "")
        self.assertEqual(str(raised.exception), "Invalid iset node, no words specified as attribute or text")

    def test_init_with_nothing(self):
        with self.assertRaises(ParserException) as raised:
            node = PatternISetNode({}, "")
        self.assertEqual(str(raised.exception), "Invalid iset node, no words specified as attribute or text")

    def test_init(self):
        node = PatternISetNode([], "test1, test2, test3")
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
        self.assertFalse(node.is_topic())
        self.assertFalse(node.is_wildcard())
        self.assertTrue(node.is_iset())

        self.assertIsNotNone(node.children)
        self.assertFalse(node.has_children())

        self.assertIsNotNone(node.words)
        self.assertEqual(3, len(node.words))
        self.assertEqual("TEST1", node.words[0])
        self.assertEqual("TEST2", node.words[1])
        self.assertEqual("TEST3", node.words[2])

        self.assertTrue(node.equivalent(PatternISetNode([], "test1, test2, test3")))

        sentence = Sentence(self._client_context, "TEST1 TEST2 TEST3")

        result = node.equals(self._client_context, sentence, 0)
        self.assertTrue(result.matched)
        result = node.equals(self._client_context, sentence, 1)
        self.assertTrue(result.matched)
        result = node.equals(self._client_context, sentence, 2)
        self.assertTrue(result.matched)
        result = node.equals(self._client_context, sentence, 3)
        self.assertFalse(result.matched)

    def test_parse_words(self):
        node = PatternISetNode([], "test1")
        self.assertIsNotNone(node)
        self.assertIsNotNone(node.words)
        self.assertEqual(1, len(node.words))
        self.assertEqual("TEST1", node.words[0])

        node = PatternISetNode([], "test1,test2")
        self.assertIsNotNone(node)
        self.assertIsNotNone(node.words)
        self.assertEqual(2, len(node.words))
        self.assertEqual("TEST1", node.words[0])
        self.assertEqual("TEST2", node.words[1])

        node = PatternISetNode([], " test1, test2 , test3 ")
        self.assertIsNotNone(node)
        self.assertIsNotNone(node.words)
        self.assertEqual(3, len(node.words))
        self.assertEqual("TEST1", node.words[0])
        self.assertEqual("TEST2", node.words[1])
        self.assertEqual("TEST3", node.words[2])

    def test_to_xml(self):
        node1 = PatternISetNode([], "test1, test2, test3")
        self.assertEqual('<iset words="TEST1. TEST2. TEST3"></iset>\n', node1.to_xml(self._client_context))

        node2 = PatternISetNode([], "test1, test2, test3", userid="testid")
        self.assertEqual('<iset words="TEST1. TEST2. TEST3"></iset>\n', node2.to_xml(self._client_context, include_user=False))
        self.assertEqual('<iset userid="testid" words="TEST1. TEST2. TEST3"></iset>\n', node2.to_xml(self._client_context, include_user=True))

    def test_to_string(self):
        node1 = PatternISetNode([], "test1, test2, test3")
        self.assertEqual(node1.to_string(verbose=False), "ISET words=[TEST1,TEST2,TEST3]")
        self.assertEqual(node1.to_string(verbose=True), "ISET [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] words=[TEST1,TEST2,TEST3]")

        node2 = PatternISetNode([], "test1, test2, test3", userid="testid")
        self.assertEqual(node2.to_string(verbose=False), "ISET words=[TEST1,TEST2,TEST3]")
        self.assertEqual(node2.to_string(verbose=True), "ISET [testid] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] words=[TEST1,TEST2,TEST3]")

    def test_equivalent(self):
        node1 = PatternISetNode([], "test1, test2, test3")
        node2 = PatternISetNode([], "test1, test2, test3")
        node3 = PatternISetNode([], "test1, test2, test3", userid="testid")

        self.assertTrue(node1.equivalent(node2))
        self.assertFalse(node1.equivalent(node3))

    def test_equals(self):
        node1 = PatternISetNode([], "test1, test2, test3")
        node2 = PatternISetNode([], "test1, test2, test3", userid="testid")
        node3 = PatternISetNode([], "test1, test2, test3", userid="testid2")

        match1 = node1.equals(self._client_context, Sentence(self._client_context, 'test1'), 0)
        self.assertIsNotNone(match1)
        self.assertTrue(match1.matched)

        match2 = node2.equals(self._client_context, Sentence(self._client_context, 'test1'), 0)
        self.assertIsNotNone(match2)
        self.assertTrue(match2.matched)

        match3 = node3.equals(self._client_context, Sentence(self._client_context, 'test1'), 0)
        self.assertIsNotNone(match3)
        self.assertFalse(match3.matched)

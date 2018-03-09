from programytest.parser.base import ParserTestsBaseClass

from programy.parser.pattern.nodes.iset import PatternISetNode
from programy.dialog.dialog import Sentence
from programy.parser.exceptions import ParserException

class PatternSetNodeTests(ParserTestsBaseClass):

    def test_init_with_text(self):
        node = PatternISetNode({}, "test1, test2, test3")
        self.assertIsNotNone(node)
        self.assertEquals("TEST1", node.words[0])
        self.assertEquals("TEST2", node.words[1])
        self.assertEquals("TEST3", node.words[2])

    def test_init_with_attribs(self):
        node = PatternISetNode({"words": "test1, test2, test3"}, "")
        self.assertIsNotNone(node)
        self.assertEquals("TEST1", node.words[0])
        self.assertEquals("TEST2", node.words[1])
        self.assertEquals("TEST3", node.words[2])

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
        self.assertEquals(3, len(node.words))
        self.assertEquals("TEST1", node.words[0])
        self.assertEquals("TEST2", node.words[1])
        self.assertEquals("TEST3", node.words[2])

        self.assertTrue(node.equivalent(PatternISetNode([], "test1, test2, test3")))

        sentence = Sentence(self._client_context.brain.tokenizer, "TEST1 TEST2 TEST3")

        result = node.equals(self._client_context, sentence, 0)
        self.assertTrue(result.matched)
        result = node.equals(self._client_context, sentence, 1)
        self.assertTrue(result.matched)
        result = node.equals(self._client_context, sentence, 2)
        self.assertTrue(result.matched)
        result = node.equals(self._client_context, sentence, 3)
        self.assertFalse(result.matched)

        self.assertEqual(node.to_string(), "ISET [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] words=[TEST1,TEST2,TEST3]")
        self.assertEqual('<iset words="TEST1. TEST2. TEST3"></iset>\n', node.to_xml(self._client_context))

    def test_parse_words(self):
        node = PatternISetNode([], "test1")
        self.assertIsNotNone(node)
        self.assertIsNotNone(node.words)
        self.assertEquals(1, len(node.words))
        self.assertEquals("TEST1", node.words[0])

        node = PatternISetNode([], "test1,test2")
        self.assertIsNotNone(node)
        self.assertIsNotNone(node.words)
        self.assertEquals(2, len(node.words))
        self.assertEquals("TEST1", node.words[0])
        self.assertEquals("TEST2", node.words[1])

        node = PatternISetNode([], " test1, test2 , test3 ")
        self.assertIsNotNone(node)
        self.assertIsNotNone(node.words)
        self.assertEquals(3, len(node.words))
        self.assertEquals("TEST1", node.words[0])
        self.assertEquals("TEST2", node.words[1])
        self.assertEquals("TEST3", node.words[2])


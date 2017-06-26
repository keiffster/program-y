from test.parser.pattern.base import PatternTestBaseClass

from programy.parser.pattern.nodes.iset import PatternISetNode
from programy.dialog import Sentence

class PatternSetNodeTests(PatternTestBaseClass):

    def test_init(self):
        node = PatternISetNode("test1, test2, test3")
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

        self.assertFalse(node.equivalent(PatternISetNode("test1, test2, test3")))

        sentence = Sentence("TEST1 TEST2 TEST3")

        result = node.equals(None, "testid", sentence, 0)
        self.assertTrue(result.matched)
        result = node.equals(None, "testid", sentence, 1)
        self.assertTrue(result.matched)
        result = node.equals(None, "testid", sentence, 2)
        self.assertTrue(result.matched)
        result = node.equals(None, "testid", sentence, 3)
        self.assertFalse(result.matched)

        self.assertEqual(node.to_string(), "ISET [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] words=[TEST1,TEST2,TEST3]")

    def test_parse_words(self):
        node = PatternISetNode("test1")
        self.assertIsNotNone(node)
        self.assertIsNotNone(node.words)
        self.assertEquals(1, len(node.words))
        self.assertEquals("TEST1", node.words[0])

        node = PatternISetNode("test1,test2")
        self.assertIsNotNone(node)
        self.assertIsNotNone(node.words)
        self.assertEquals(2, len(node.words))
        self.assertEquals("TEST1", node.words[0])
        self.assertEquals("TEST2", node.words[1])

        node = PatternISetNode(" test1, test2 , test3 ")
        self.assertIsNotNone(node)
        self.assertIsNotNone(node.words)
        self.assertEquals(3, len(node.words))
        self.assertEquals("TEST1", node.words[0])
        self.assertEquals("TEST2", node.words[1])
        self.assertEquals("TEST3", node.words[2])


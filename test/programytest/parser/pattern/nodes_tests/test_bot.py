from programytest.parser.base import ParserTestsBaseClass

from programy.parser.pattern.nodes.bot import PatternBotNode
from programy.dialog.dialog import Sentence
from programy.parser.exceptions import ParserException

class PatternBotNodeTests(ParserTestsBaseClass):

    def test_init_with_text(self):
        node = PatternBotNode({}, "test1")
        self.assertIsNotNone(node)
        self.assertEqual("test1", node.property)

    def test_init_with_attribs_name(self):
        node = PatternBotNode({"name": "test1"}, "")
        self.assertIsNotNone(node)
        self.assertEqual("test1", node.property)

    def test_init_with_attribs_property(self):
        node = PatternBotNode({"property": "test1"}, "")
        self.assertIsNotNone(node)
        self.assertEqual("test1", node.property)

    def test_init_with_invalid_attribs(self):
        with self.assertRaises(ParserException) as raised:
            node = PatternBotNode({"unknwon": "test1"}, "")
        self.assertEqual(str(raised.exception), "Invalid bot node, neither name or property specified as attribute or text")

    def test_init_with_nothing(self):
        with self.assertRaises(ParserException) as raised:
            node = PatternBotNode({}, "")
        self.assertEqual(str(raised.exception), "Invalid bot node, neither name or property specified as attribute or text")

    def test_init(self):

        self._client_context.brain.properties.add_property("test1", "value1")

        node = PatternBotNode([], "test1")
        self.assertIsNotNone(node)

        self.assertFalse(node.is_root())
        self.assertFalse(node.is_priority())
        self.assertFalse(node.is_wildcard())
        self.assertFalse(node.is_zero_or_more())
        self.assertFalse(node.is_one_or_more())
        self.assertFalse(node.is_set())
        self.assertTrue(node.is_bot())
        self.assertFalse(node.is_template())
        self.assertFalse(node.is_that())
        self.assertFalse(node.is_topic())
        self.assertFalse(node.is_wildcard())

        self.assertTrue(node.equivalent(PatternBotNode([], "test1")))
        self.assertFalse(node.equivalent(PatternBotNode([], "test2")))

        sentence = Sentence(self._client_context.brain.tokenizer, "value1 value2")

        result = node.equals(self._client_context, sentence, 0)
        self.assertTrue(result.matched)
        self.assertEquals(0, result.word_no)

        result = node.equals(self._client_context, sentence, 1)
        self.assertFalse(result.matched)
        self.assertEquals(1, result.word_no)

        self.assertEqual(node.to_string(), "BOT [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] property=[test1]")
        self.assertEqual('<bot property="test1">\n</bot>', node.to_xml(self._client_context))


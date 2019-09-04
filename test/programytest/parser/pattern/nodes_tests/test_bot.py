from programytest.parser.base import ParserTestsBaseClass

from programy.parser.pattern.nodes.bot import PatternBotNode
from programy.dialog.sentence import Sentence
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

        node = PatternBotNode({}, "test1")
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

        sentence = Sentence(self._client_context, "value1 value2")

        result = node.equals(self._client_context, sentence, 0)
        self.assertTrue(result.matched)
        self.assertEqual(0, result.word_no)

        result = node.equals(self._client_context, sentence, 1)
        self.assertFalse(result.matched)
        self.assertEqual(1, result.word_no)

        self.assertEqual(node.to_string(), "BOT [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] property=[test1]")
        self.assertEqual('<bot property="test1">\n</bot>', node.to_xml(self._client_context))

    def test_to_xml(self):
        bot1 = PatternBotNode({}, "bot1")
        self.assertEqual('<bot property="bot1">\n</bot>', bot1.to_xml(self._client_context, include_user=False))
        self.assertEqual('<bot userid="*" property="bot1">\n</bot>', bot1.to_xml(self._client_context, include_user=True))

        bot2 = PatternBotNode({"name": "test"}, "bot2")
        self.assertEqual('<bot property="test">\n</bot>', bot2.to_xml(self._client_context, include_user=False))
        self.assertEqual('<bot userid="*" property="test">\n</bot>', bot2.to_xml(self._client_context, include_user=True))

        bot3 = PatternBotNode({"property": "test"}, "bot3")
        self.assertEqual('<bot property="test">\n</bot>', bot3.to_xml(self._client_context, include_user=False))
        self.assertEqual('<bot userid="*" property="test">\n</bot>', bot3.to_xml(self._client_context, include_user=True))

        bot4 = PatternBotNode({}, "bot4", userid="testid")
        self.assertEqual('<bot property="bot4">\n</bot>', bot4.to_xml(self._client_context, include_user=False))
        self.assertEqual('<bot userid="testid" property="bot4">\n</bot>', bot4.to_xml(self._client_context, include_user=True))

        bot5 = PatternBotNode({"name": "test"}, "bot5", userid="testid")
        self.assertEqual('<bot property="test">\n</bot>', bot5.to_xml(self._client_context, include_user=False))
        self.assertEqual('<bot userid="testid" property="test">\n</bot>', bot5.to_xml(self._client_context, include_user=True))

        bot6 = PatternBotNode({"property": "test"}, "bot6", userid="testid")
        self.assertEqual('<bot property="test">\n</bot>', bot6.to_xml(self._client_context, include_user=False))
        self.assertEqual('<bot userid="testid" property="test">\n</bot>', bot6.to_xml(self._client_context, include_user=True))

    def test_to_string(self):
        bot1 = PatternBotNode({}, "bot1")
        self.assertEqual('BOT property=[bot1]', bot1.to_string(verbose=False))
        self.assertEqual('BOT [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] property=[bot1]', bot1.to_string(verbose=True))

        bot2 = PatternBotNode({"name": "test"}, "bot2")
        self.assertEqual('BOT property=[test]', bot2.to_string(verbose=False))
        self.assertEqual('BOT [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] property=[test]', bot2.to_string(verbose=True))

        bot3 = PatternBotNode({"property": "test"}, "bot3")
        self.assertEqual('BOT property=[test]', bot3.to_string(verbose=False))
        self.assertEqual('BOT [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] property=[test]', bot3.to_string(verbose=True))

        bot4 = PatternBotNode({}, "bot4", userid="testid")
        self.assertEqual('BOT property=[bot4]', bot4.to_string(verbose=False))
        self.assertEqual('BOT [testid] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] property=[bot4]', bot4.to_string(verbose=True))

        bot5 = PatternBotNode({"name": "test"}, "bot5", userid="testid")
        self.assertEqual('BOT property=[test]', bot5.to_string(verbose=False))
        self.assertEqual('BOT [testid] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] property=[test]', bot5.to_string(verbose=True))

        bot6 = PatternBotNode({"property": "test"}, "bot6", userid="testid")
        self.assertEqual('BOT property=[test]', bot6.to_string(verbose=False))
        self.assertEqual('BOT [testid] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] property=[test]', bot6.to_string(verbose=True))

    def test_equals_text(self):
        bot1 = PatternBotNode({}, "bot1")
        bot2 = PatternBotNode({}, "bot1")
        bot3 = PatternBotNode({}, "bot1", userid="testid")

        self.assertTrue(bot1.equivalent(bot2))
        self.assertFalse(bot1.equivalent(bot3))

    def test_equals_name(self):
        bot4 = PatternBotNode({"name": "test"}, "bot1")
        bot5 = PatternBotNode({"name": "test"}, "bot1")
        bot6 = PatternBotNode({"name": "test"}, "bot1", userid="testid")

        self.assertTrue(bot4.equivalent(bot5))
        self.assertFalse(bot4.equivalent(bot6))

    def test_equals_property(self):
        bot7 = PatternBotNode({"property": "test"}, "bot1")
        bot8 = PatternBotNode({"property": "test"}, "bot1")
        bot9 = PatternBotNode({"property": "test"}, "bot1", userid="testid")

        self.assertTrue(bot7.equivalent(bot8))
        self.assertFalse(bot7.equivalent(bot9))

    def test_equivalent_text(self):
        self._client_context.brain.properties.add_property("test1", "value1")

        bot1 = PatternBotNode({}, "test1")
        bot2 = PatternBotNode({}, "test1", userid="testid")
        bot3 = PatternBotNode({}, "test1", userid="testid2")

        match1 = bot1.equals(self._client_context, Sentence(self._client_context, 'value1'), 0)
        self.assertIsNotNone(match1)
        self.assertTrue(match1.matched)

        match2 = bot2.equals(self._client_context, Sentence(self._client_context, 'value1'), 0)
        self.assertIsNotNone(match2)
        self.assertTrue(match2.matched)

        match3 = bot3.equals(self._client_context, Sentence(self._client_context, 'value1'), 0)
        self.assertIsNotNone(match3)
        self.assertFalse(match3.matched)

    def test_equivalent_name(self):
        self._client_context.brain.properties.add_property("test1", "value1")

        bot1 = PatternBotNode({"name": "test1"}, None)
        bot2 = PatternBotNode({"name": "test1"}, None, userid="testid")
        bot3 = PatternBotNode({"name": "test1"}, None, userid="testid2")

        match1 = bot1.equals(self._client_context, Sentence(self._client_context, 'value1'), 0)
        self.assertIsNotNone(match1)
        self.assertTrue(match1.matched)

        match2 = bot2.equals(self._client_context, Sentence(self._client_context, 'value1'), 0)
        self.assertIsNotNone(match2)
        self.assertTrue(match2.matched)

        match3 = bot3.equals(self._client_context, Sentence(self._client_context, 'value1'), 0)
        self.assertIsNotNone(match3)
        self.assertFalse(match3.matched)

    def test_equivalent_property(self):
        self._client_context.brain.properties.add_property("test1", "value1")

        bot1 = PatternBotNode({"property": "test1"}, None)
        bot2 = PatternBotNode({"property": "test1"}, None, userid="testid")
        bot3 = PatternBotNode({"property": "test1"}, None, userid="testid2")

        match1 = bot1.equals(self._client_context, Sentence(self._client_context, 'value1'), 0)
        self.assertIsNotNone(match1)
        self.assertTrue(match1.matched)

        match2 = bot2.equals(self._client_context, Sentence(self._client_context, 'value1'), 0)
        self.assertIsNotNone(match2)
        self.assertTrue(match2.matched)

        match3 = bot3.equals(self._client_context, Sentence(self._client_context, 'value1'), 0)
        self.assertIsNotNone(match3)
        self.assertFalse(match3.matched)


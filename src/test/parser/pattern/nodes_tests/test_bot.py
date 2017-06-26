from test.parser.pattern.base import PatternTestBaseClass

from programy.parser.pattern.nodes.bot import PatternBotNode
from programy.dialog import Sentence

class PatternBotNodeTests(PatternTestBaseClass):

    def test_init(self):

        self.bot.brain.properties.add_property("test1", "value1")

        node = PatternBotNode("test1")
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

        self.assertTrue(node.equivalent(PatternBotNode("test1")))
        self.assertFalse(node.equivalent(PatternBotNode("test2")))

        sentence = Sentence("value1 value2")

        result = node.equals(self.bot, "testid", sentence, 0)
        self.assertTrue(result.matched)
        self.assertEquals(0, result.word_no)
        result = node.equals(self.bot, "testid", sentence, 1)
        self.assertFalse(result.matched)
        self.assertEquals(1, result.word_no)

        self.assertEqual(node.to_string(), "BOT [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] property=[test1]")


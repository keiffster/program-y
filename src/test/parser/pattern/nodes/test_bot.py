from test.parser.pattern.nodes.base import PatternTestBaseClass
from programy.parser.pattern.nodes.bot import PatternBotNode

class PatternBotNodeTests(PatternTestBaseClass):

    def test_init(self):

        self.bot.brain.properties.set_property("test1", "value1")

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

        self.assertTrue(node.equals(self.bot, "testid", "value1"))
        self.assertFalse(node.equals(self.bot, "testid", "value2"))

        self.assertEqual(node.to_string(), "BOT [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] property=[test1]")


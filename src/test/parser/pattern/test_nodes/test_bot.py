from test.parser.pattern.test_nodes.base import PatternTestBaseClass
from programy.parser.pattern.nodes.bot import PatternBotNode

class PatternBotNodeTests(PatternTestBaseClass):

    def test_init(self):
        node = PatternBotNode("test1")
        self.assertIsNotNone(node)

        self.assertFalse(node.is_root())
        self.assertFalse(node.is_priority())
        self.assertFalse(node.is_wildcard())
        self.assertFalse(node.is_zero_or_more())
        self.assertFalse(node.is_one_or_more())
        self.assertIsNotNone(node.children)
        self.assertFalse(node.has_children())

        self.assertTrue(node.equivalent(PatternBotNode("test1")))
        self.assertFalse(node.is_root())
        self.assertEqual(node.to_string(), "BOT [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] property=[test1]")


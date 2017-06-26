from test.parser.pattern.base import PatternTestBaseClass

from programy.parser.pattern.nodes.base import PatternNode
from programy.parser.pattern.nodes.oneormore import PatternOneOrMoreWildCardNode
from programy.parser.pattern.nodes.zeroormore import PatternZeroOrMoreWildCardNode

class PatternBotNodeTests(PatternTestBaseClass):

    def test_init(self):

        node = PatternNode()
        self.assertIsNotNone(node)

        self.assertFalse(node.is_root())

        self.assertEquals(0, len(node.priority_words))
        self.assertFalse(node.has_priority_words())
        self.assertFalse(node.is_priority())

        self.assertIsNone(node.arrow)
        self.assertIsNone(node.hash)
        self.assertIsNone(node.underline)
        self.assertIsNone(node.star)

        self.assertFalse(node.has_wildcard())
        self.assertFalse(node.has_zero_or_more())
        self.assertFalse(node.has_0ormore_arrow())
        self.assertFalse(node.has_0ormore_hash())
        self.assertFalse(node.has_one_or_more())
        self.assertFalse(node.has_1ormore_star())
        self.assertFalse(node.has_1ormore_underline())
        self.assertFalse(node.is_wildcard())
        self.assertFalse(node.is_zero_or_more())
        self.assertFalse(node.is_one_or_more())

        self.assertEquals(0, len(node.children))
        self.assertFalse(node.has_children())
        self.assertFalse(node.has_nodes())

        self.assertIsNone(node.topic)
        self.assertFalse(node.is_topic())
        self.assertFalse(node.has_topic())

        self.assertIsNone(node.that)
        self.assertFalse(node.is_that())
        self.assertFalse(node.has_that())

        self.assertIsNone(node.template)
        self.assertFalse(node.is_template())
        self.assertFalse(node.has_template())

        self.assertFalse(node.is_set())

        self.assertFalse(node.is_bot())

    def test_wildcard(self):

        node = PatternNode()
        self.assertIsNotNone(node)

        self.assertFalse(node.has_wildcard())
        self.assertFalse(node.has_zero_or_more())
        self.assertFalse(node.has_one_or_more())

        node = PatternNode()
        node._0ormore_arrow = PatternZeroOrMoreWildCardNode("^")
        self.assertTrue(node.has_wildcard())
        self.assertTrue(node.has_zero_or_more())
        self.assertFalse(node.has_one_or_more())

        node = PatternNode()
        node._0ormore_hash = PatternZeroOrMoreWildCardNode("#")
        self.assertTrue(node.has_wildcard())
        self.assertTrue(node.has_zero_or_more())
        self.assertFalse(node.has_one_or_more())

        node = PatternNode()
        node._1ormore_star = PatternOneOrMoreWildCardNode("*")
        self.assertTrue(node.has_wildcard())
        self.assertFalse(node.has_zero_or_more())
        self.assertTrue(node.has_one_or_more())

        node = PatternNode()
        node._1ormore_underline = PatternOneOrMoreWildCardNode("_")
        self.assertTrue(node.has_wildcard())
        self.assertFalse(node.has_zero_or_more())
        self.assertTrue(node.has_one_or_more())

    def test_has_nodes(self):

        node = PatternNode()
        self.assertIsNotNone(node)
        self.assertFalse(node.has_nodes())

        node = PatternNode()
        node._children.append(PatternNode())
        self.assertTrue(node.has_nodes())

        node = PatternNode()
        node._priority_words.append(PatternNode())
        self.assertTrue(node.has_nodes())

        node = PatternNode()
        node._1ormore_underline = PatternOneOrMoreWildCardNode("_")
        self.assertTrue(node.has_nodes())

    def test_equals_ignore_case(self):

        node = PatternNode()
        self.assertIsNotNone(node)

        self.assertTrue(node.equals_ignore_case(self.bot, "testid", "test", "test"))
        self.assertTrue(node.equals_ignore_case(self.bot, "testid", "Test", "test"))
        self.assertTrue(node.equals_ignore_case(self.bot, "testid", "test", "Test"))
        self.assertTrue(node.equals_ignore_case(self.bot, "testid", "TEST", "test"))
        self.assertTrue(node.equals_ignore_case(self.bot, "testid", "test", "TEST"))


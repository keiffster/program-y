from programy.dialog import Sentence
from programy.parser.pattern.nodes import *
from programy.parser.template.nodes import TemplateNode

from test.parser.pattern.base import PatternTestBaseClass
        
class PatternNodeTests(PatternTestBaseClass):

    def test_init(self):
        node = PatternNode()
        self.assertIsNotNone(node)
        self.assertFalse(node.is_root())
        self.assertFalse(node.is_priority())
        self.assertFalse(node.is_wildcard())
        self.assertFalse(node.is_zero_or_more())
        self.assertFalse(node.is_one_or_more())
        self.assertFalse(node.has_children())
        self.assertIsNotNone(node.children)

        self.assertFalse(node.equivalent(PatternNode()))
        self.assertEqual(node.to_string(), "NODE [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)]")

        node.add_child(PatternNode())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.to_string(), "NODE [P(0)^(0)#(0)C(1)_(0)*(0)To(0)Th(0)Te(0)]")

    def test_add_child(self):

        node = PatternNode()

        priority_word1 = PatternPriorityWordNode("pword")
        priority_word2 = PatternPriorityWordNode("pword")
        node.add_child(priority_word1)
        new_node = node.add_child(priority_word2)
        self.assertEqual(new_node, priority_word1)

        arrow_node1 = PatternZeroOrMoreWildCardNode("^")
        arrow_node2 = PatternZeroOrMoreWildCardNode("^")
        node.add_child(arrow_node1)
        new_node = node.add_child(arrow_node2)
        self.assertEqual(new_node, arrow_node1)


class PatternRootNodeTests(PatternTestBaseClass):

    def test_init(self):
        node = PatternRootNode()
        self.assertIsNotNone(node)

        self.assertTrue(node.is_root())
        self.assertFalse(node.is_priority())
        self.assertFalse(node.is_wildcard())
        self.assertFalse(node.is_zero_or_more())
        self.assertFalse(node.is_one_or_more())
        self.assertIsNotNone(node.children)
        self.assertFalse(node.has_children())

        self.assertTrue(node.equivalent(PatternRootNode()))
        self.assertEqual(node.to_string(), "ROOT [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)]")

        node.add_child(PatternNode())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.to_string(), "ROOT [P(0)^(0)#(0)C(1)_(0)*(0)To(0)Th(0)Te(0)]")

    def test_multiple_roots(self):
        node1 = PatternRootNode()
        node2 = PatternRootNode()

        with self.assertRaises(ParserException) as raised:
            node1.can_add(node2)
        self.assertTrue(str(raised.exception).startswith("Cannot add root node to existing root node"))

    def test_root_added_to_child(self):
        node1 = PatternWordNode("test")
        node2 = PatternRootNode()

        with self.assertRaises(ParserException) as raised:
            node1.can_add(node2)
        self.assertTrue(str(raised.exception).startswith("Cannot add root node to child node"))


class PatternTopicNodeTests(PatternTestBaseClass):

    def test_init(self):
        node = PatternTopicNode()
        self.assertIsNotNone(node)

        self.assertFalse(node.is_root())
        self.assertFalse(node.is_priority())
        self.assertFalse(node.is_wildcard())
        self.assertFalse(node.is_zero_or_more())
        self.assertFalse(node.is_one_or_more())
        self.assertIsNotNone(node.children)
        self.assertFalse(node.has_children())

        self.assertTrue(node.equivalent(PatternTopicNode()))
        self.assertEqual(node.to_string(), "TOPIC [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)]")

    def test_topic_to_root(self):
        node1 = PatternRootNode()
        node2 = PatternTopicNode()

        with self.assertRaises(ParserException) as raised:
            node1.can_add(node2)
        self.assertEqual(str(raised.exception), "Cannot add topic node to root node")

    def test_multiple_topics(self):
        node1 = PatternTopicNode()
        node2 = PatternTopicNode()

        with self.assertRaises(ParserException) as raised:
            node1.can_add(node2)
        self.assertEqual(str(raised.exception), "Cannot add topic node to topic node")


class PatternThatNodeTests(PatternTestBaseClass):

    def test_init(self):
        node = PatternThatNode()
        self.assertIsNotNone(node)

        self.assertFalse(node.is_root())
        self.assertFalse(node.is_priority())
        self.assertFalse(node.is_wildcard())
        self.assertFalse(node.is_zero_or_more())
        self.assertFalse(node.is_one_or_more())
        self.assertIsNotNone(node.children)
        self.assertFalse(node.has_children())

        self.assertTrue(node.equivalent(PatternThatNode()))
        self.assertEqual(node.to_string(), "THAT [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)]")

    def test_that_to_root(self):
        node1 = PatternRootNode()
        node2 = PatternThatNode()

        with self.assertRaises(ParserException) as raised:
            node1.can_add(node2)
        self.assertEqual(str(raised.exception), "Cannot add that node to root node")

    def test_multiple_thats(self):
        node1 = PatternThatNode()
        node2 = PatternThatNode()

        with self.assertRaises(ParserException) as raised:
            node1.can_add(node2)
        self.assertEqual(str(raised.exception), "Cannot add that node to that node")


class PatternTemplateNodeTests(PatternTestBaseClass):

    def test_init(self):

        node = PatternTemplateNode(TemplateNode())
        self.assertIsNotNone(node)

        self.assertFalse(node.is_root())
        self.assertFalse(node.is_priority())
        self.assertFalse(node.is_wildcard())
        self.assertFalse(node.is_zero_or_more())
        self.assertFalse(node.is_one_or_more())
        self.assertIsNotNone(node.children)
        self.assertFalse(node.has_children())

        self.assertTrue(node.equivalent(PatternTemplateNode(TemplateNode())))
        self.assertEqual(node.to_string(), "PTEMPLATE [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(1)] ")

    def test_template_to_root(self):
        node1 = PatternRootNode()
        node2 = PatternTemplateNode(TemplateNode())

        with self.assertRaises(ParserException) as raised:
            node1.can_add(node2)
        self.assertEqual(str(raised.exception), "Cannot add template node to root node")

    def test_multiple_templates(self):
        node1 = PatternTemplateNode(TemplateNode())
        node2 = PatternTemplateNode(TemplateNode())

        with self.assertRaises(ParserException) as raised:
            node1.can_add(node2)
        self.assertEqual(str(raised.exception), "Cannot add template node to template node")


class PatternWordNodeTests(PatternTestBaseClass):

    def test_init(self):
        node = PatternWordNode("test1")

        self.assertFalse(node.is_root())
        self.assertFalse(node.is_priority())
        self.assertFalse(node.is_wildcard())
        self.assertFalse(node.is_zero_or_more())
        self.assertFalse(node.is_one_or_more())
        self.assertIsNotNone(node.children)
        self.assertFalse(node.has_children())

        self.assertTrue(node.equivalent(PatternWordNode("test1")))
        self.assertFalse(node.is_root())
        self.assertEqual(node.to_string(), "WORD [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] word=[test1]")

        self.assertTrue(node.matches(self.bot, self.clientid, "test1"))

        node.add_child(PatternWordNode("test2"))
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.to_string(), "WORD [P(0)^(0)#(0)C(1)_(0)*(0)To(0)Th(0)Te(0)] word=[test1]")

        self.assertIsNotNone(node.matches(self.bot, self.clientid, Sentence("test1")))

class PatternPriorityWordNodeTests(PatternTestBaseClass):

    def test_init(self):
        node = PatternPriorityWordNode("test1")
        self.assertIsNotNone(node)

        self.assertFalse(node.is_root())
        self.assertTrue(node.is_priority())
        self.assertFalse(node.is_wildcard())
        self.assertFalse(node.is_zero_or_more())
        self.assertFalse(node.is_one_or_more())
        self.assertIsNotNone(node.children)
        self.assertFalse(node.has_children())

        self.assertTrue(node.equivalent(PatternPriorityWordNode("test1")))
        self.assertFalse(node.is_root())
        self.assertEqual(node.to_string(), "PWORD [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] word=[test1]")

        self.assertTrue(node.matches(self.bot, self.clientid, "test1"))

        node.add_child(PatternWordNode("test2"))
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.to_string(), "PWORD [P(0)^(0)#(0)C(1)_(0)*(0)To(0)Th(0)Te(0)] word=[test1]")

        self.assertTrue(node.matches(self.bot, self.clientid, "test1"))

class PatternSetNodeTests(PatternTestBaseClass):

    def test_init(self):
        node = PatternSetNode("test1")
        self.assertIsNotNone(node)

        self.assertFalse(node.is_root())
        self.assertFalse(node.is_priority())
        self.assertFalse(node.is_wildcard())
        self.assertFalse(node.is_zero_or_more())
        self.assertFalse(node.is_one_or_more())
        self.assertIsNotNone(node.children)
        self.assertFalse(node.has_children())

        self.assertTrue(node.equivalent(PatternSetNode("test1")))
        self.assertFalse(node.is_root())
        self.assertEqual(node.to_string(), "SET [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] name=[TEST1]")

        self.bot.brain.sets._sets["TEST1"] = ["val1", "val2", "val3"]

        self.assertTrue(node.matches(self.bot, self.clientid, "val1"))
        self.assertTrue(node.matches(self.bot, self.clientid, "val2"))
        self.assertFalse(node.matches(self.bot, self.clientid, "val4"))

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

        self.bot.brain.properties._properties["test1"] = "val1"

        self.assertTrue(node.matches(self.bot, self.clientid, "val1"))
        self.assertFalse(node.matches(self.bot, self.clientid, "val4"))

class PatternZeroOrMoreWildCardNodeTests(PatternTestBaseClass):

    def test_invalid_wildcard(self):
        with self.assertRaises(ParserException) as raised:
            node = PatternZeroOrMoreWildCardNode("X")
            self.assertIsNone(node)

    def test_init(self):
        node = PatternZeroOrMoreWildCardNode("#")

        self.assertFalse(node.is_root())
        self.assertFalse(node.is_priority())
        self.assertTrue(node.is_wildcard())
        self.assertTrue(node.is_zero_or_more())
        self.assertFalse(node.is_one_or_more())
        self.assertIsNotNone(node.children)
        self.assertFalse(node.has_children())

        self.assertEqual(node.wildcard, "#")

        self.assertTrue(node.equivalent(PatternZeroOrMoreWildCardNode("#")))
        self.assertFalse(node.is_root())
        self.assertEqual(node.to_string(), "ZEROORMORE [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] wildcard=[#]")

        node = PatternZeroOrMoreWildCardNode("^")
        self.assertIsNotNone(node)

        self.assertEqual(node.wildcard, "^")

        self.assertTrue(node.equivalent(PatternZeroOrMoreWildCardNode("^")))
        self.assertFalse(node.is_root())
        self.assertEqual(node.to_string(), "ZEROORMORE [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] wildcard=[^]")

class PatternOneOrMoreWildCardNodeTests(PatternTestBaseClass):

    def test_invalid_wildcard(self):
        with self.assertRaises(ParserException) as raised:
            node = PatternOneOrMoreWildCardNode("X")
            self.assertIsNone(node)

    def test_init(self):
        node = PatternOneOrMoreWildCardNode("*")
        self.assertIsNotNone(node)

        self.assertFalse(node.is_root())
        self.assertFalse(node.is_priority())
        self.assertTrue(node.is_wildcard())
        self.assertFalse(node.is_zero_or_more())
        self.assertTrue(node.is_one_or_more())

        self.assertIsNotNone(node.children)
        self.assertFalse(node.has_children())

        self.assertEqual(node.wildcard, "*")

        self.assertTrue(node.equivalent(PatternOneOrMoreWildCardNode("*")))
        self.assertFalse(node.is_root())
        self.assertEqual(node.to_string(), "ONEORMORE [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] wildcard=[*]")

        node = PatternOneOrMoreWildCardNode("_")
        self.assertIsNotNone(node)

        self.assertEqual(node.wildcard, "_")

        self.assertTrue(node.equivalent(PatternOneOrMoreWildCardNode("_")))
        self.assertFalse(node.is_root())
        self.assertEqual(node.to_string(), "ONEORMORE [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] wildcard=[_]")


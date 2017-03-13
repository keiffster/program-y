from test.parser.pattern.test_nodes.base import PatternTestBaseClass
from programy.dialog import Sentence
from programy.parser.pattern.graph import PatternGraph
from programy.parser.pattern.nodes import *
from programy.parser.template.nodes import *


class PatternGraphTests(PatternTestBaseClass):

    def test_init_graph(self):
        graph = PatternGraph()
        self.assertIsNotNone(graph)
        self.assertIsNotNone(graph.root)

    def test_add_pattern_with_whitepsace(self):
        graph = PatternGraph()
        topic_element = ET.fromstring('<topic>*</topic>')
        that_element = ET.fromstring('<that>*</that>')
        template_graph_root = None

        element = ET.fromstring("<pattern>\nthis\n that\n the other</pattern>")
        graph.add_pattern_to_graph(element, topic_element, that_element, template_graph_root)

        root = graph.root
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 1)
        self.assertIsInstance(root.children[0], PatternWordNode)

        this = root.children[0]
        self.assertIsNotNone(this)
        self.assertEqual(this.word, "this")
        self.assertEqual(len(this.children), 1)

        that = this.children[0]
        self.assertIsNotNone(that)
        self.assertEqual(that.word, "that")
        self.assertEqual(len(that.children), 1)

        the = that.children[0]
        self.assertIsNotNone(the)
        self.assertEqual(the.word, "the")
        self.assertEqual(len(the.children), 1)

        other = the.children[0]
        self.assertIsNotNone(other)
        self.assertEqual(other.word, "other")
        self.assertEqual(len(other.children), 0)

    def test_add_pattern_to_graph_basic(self):
        graph = PatternGraph()
        topic_element = ET.fromstring('<topic>*</topic>')
        that_element = ET.fromstring('<that>*</that>')
        template_graph_root = None

        element = ET.fromstring("<pattern>test1</pattern>")
        graph.add_pattern_to_graph(element, topic_element, that_element, template_graph_root)

        self.assertIsNotNone(graph.root)
        self.assertIsNotNone(graph.root.children)
        self.assertEqual(len(graph.root.children), 1)
        self.assertIsInstance(graph.root.children[0], PatternWordNode)
        self.assertEqual(graph.root.children[0].word, "test1")

        element = ET.fromstring("<pattern>test2</pattern>")
        graph.add_pattern_to_graph(element, topic_element, that_element, template_graph_root)

        self.assertIsNotNone(graph.root)
        self.assertIsNotNone(graph.root.children)
        self.assertEqual(len(graph.root.children), 2)
        self.assertIsInstance(graph.root.children[0], PatternWordNode)
        self.assertEqual(graph.root.children[0].word, "test1")
        self.assertIsInstance(graph.root.children[0], PatternWordNode)
        self.assertEqual(graph.root.children[1].word, "test2")

    def test_add_pattern_to_graph_multi_word(self):
        graph = PatternGraph()
        topic_element = ET.fromstring('<topic>*</topic>')
        that_element = ET.fromstring('<that>*</that>')
        template_graph_root = None

        element1 = ET.fromstring("<pattern>test1 test2</pattern>")
        graph.add_pattern_to_graph(element1, topic_element, that_element, template_graph_root)

        self.assertIsNotNone(graph.root)
        self.assertIsNotNone(graph.root.children)
        self.assertEqual(len(graph.root.children), 1)
        self.assertIsInstance(graph.root.children[0], PatternWordNode)
        self.assertEqual(graph.root.children[0].word, "test1")

        self.assertEqual(len(graph.root.children[0].children), 1)
        self.assertIsInstance(graph.root.children[0].children[0], PatternWordNode)
        self.assertEqual(graph.root.children[0].children[0].word, "test2")

        element2 = ET.fromstring("<pattern>test1 test3 test4</pattern>")
        graph.add_pattern_to_graph(element2, topic_element, that_element, template_graph_root)

        self.assertIsNotNone(graph.root)
        self.assertIsNotNone(graph.root.children)
        self.assertEqual(len(graph.root.children), 1)
        self.assertIsInstance(graph.root.children[0], PatternWordNode)
        self.assertEqual(graph.root.children[0].word, "test1")

        self.assertEqual(len(graph.root.children[0].children), 2)
        self.assertIsInstance(graph.root.children[0].children[0], PatternWordNode)
        self.assertEqual(graph.root.children[0].children[0].word, "test2")
        self.assertIsInstance(graph.root.children[0].children[1], PatternWordNode)
        self.assertEqual(graph.root.children[0].children[1].word, "test3")

        self.assertEqual(len(graph.root.children[0].children[1].children), 1)
        self.assertIsInstance(graph.root.children[0].children[1].children[0], PatternWordNode)
        self.assertEqual(graph.root.children[0].children[1].children[0].word, "test4")

    def test_add_pattern_to_graph_basic_set_text(self):
        graph = PatternGraph()
        topic_element = ET.fromstring('<topic>*</topic>')
        that_element = ET.fromstring('<that>*</that>')
        template_graph_root = None

        self.bot.brain.sets._sets["SET1"] = ["VAL1", "VAL2", "VAL3", "VAL5"]

        element = ET.fromstring('<pattern><set>set1</set> IS A VALUE</pattern>')
        graph.add_pattern_to_graph(element, topic_element, that_element, template_graph_root)
        
        self.assertIsNotNone(graph.root)
        self.assertIsNotNone(graph.root.children)
        self.assertEqual(len(graph.root.children), 1)
        self.assertIsInstance(graph.root.children[0], PatternSetNode)
        self.assertEqual(graph.root.children[0].word, "SET1")

    def test_add_pattern_to_graph_basic_set_name_attrib(self):
        graph = PatternGraph()
        topic_element = ET.fromstring('<topic>*</topic>')
        that_element = ET.fromstring('<that>*</that>')
        template_graph_root = None

        self.bot.brain.sets._sets["SET1"] = ["val1", "val2", "val3", "val5"]

        element = ET.fromstring('<pattern><set name="set1" /></pattern>')
        graph.add_pattern_to_graph(element, topic_element, that_element, template_graph_root)
        
        self.assertIsNotNone(graph.root)
        self.assertIsNotNone(graph.root.children)
        self.assertEqual(len(graph.root.children), 1)
        self.assertIsInstance(graph.root.children[0], PatternSetNode)
        self.assertEqual(graph.root.children[0].word, "SET1")

    def test_add_pattern_to_graph_basic_bot_text(self):
        graph = PatternGraph()
        topic_element = ET.fromstring('<topic>*</topic>')
        that_element = ET.fromstring('<that>*</that>')
        template_graph_root = None

        self.bot.brain.properties._properties['bot1'] = 'val1'

        element = ET.fromstring('<pattern><bot>bot1</bot></pattern>')
        graph.add_pattern_to_graph(element, topic_element, that_element, template_graph_root)
        
        self.assertIsNotNone(graph.root)
        self.assertIsNotNone(graph.root.children)
        self.assertEqual(len(graph.root.children), 1)
        self.assertIsInstance(graph.root.children[0], PatternBotNode)
        self.assertEqual(graph.root.children[0].word, "bot1")

    def test_add_pattern_to_graph_basic_bot_name_attrib(self):
        graph = PatternGraph()
        topic_element = ET.fromstring('<topic>*</topic>')
        that_element = ET.fromstring('<that>*</that>')
        template_graph_root = None

        self.bot.brain.properties._properties['bot1'] = 'val1'

        element = ET.fromstring('<pattern><bot name="bot1" /></pattern>')
        graph.add_pattern_to_graph(element, topic_element, that_element, template_graph_root)
        
        self.assertIsNotNone(graph.root)
        self.assertIsNotNone(graph.root.children)
        self.assertEqual(len(graph.root.children), 1)
        self.assertIsInstance(graph.root.children[0], PatternBotNode)
        self.assertEqual(graph.root.children[0].word, "bot1")

    def test_add_pattern_to_graph_word_set_bot(self):
        graph = PatternGraph()
        topic_element = ET.fromstring('<topic>*</topic>')
        that_element = ET.fromstring('<that>*</that>')
        template_graph_root = None

        self.bot.brain.sets._sets["SET1"] = ["val1", "val2", "val3", "val5"]
        self.bot.brain.properties._properties['bot1'] = 'val1'

        element = ET.fromstring('<pattern>test1 test2 <set name="SET1" /> test4 <bot name="bot1" /> test6</pattern>')
        graph.add_pattern_to_graph(element, topic_element, that_element, template_graph_root)
        
        self.assertIsNotNone(graph.root)

        self.assertIsNotNone(graph.root.children)
        self.assertEqual(len(graph.root.children), 1)
        self.assertIsInstance(graph.root.children[0], PatternWordNode)
        self.assertEqual(graph.root.children[0].word, "test1")

        self.assertIsNotNone(graph.root.children[0].children)
        self.assertEqual(len(graph.root.children[0].children), 1)
        self.assertIsInstance(graph.root.children[0].children[0], PatternWordNode)
        self.assertEqual(graph.root.children[0].children[0].word, "test2")

        self.assertIsNotNone(graph.root.children[0].children[0].children)
        self.assertEqual(len(graph.root.children[0].children[0].children), 1)
        self.assertIsInstance(graph.root.children[0].children[0].children[0], PatternSetNode)
        self.assertEqual(graph.root.children[0].children[0].children[0].word, "SET1")

        self.assertIsNotNone(graph.root.children[0].children[0].children[0].children)
        self.assertEqual(len(graph.root.children[0].children[0].children[0].children), 1)
        self.assertIsInstance(graph.root.children[0].children[0].children[0].children[0], PatternWordNode)
        self.assertEqual(graph.root.children[0].children[0].children[0].children[0].word, "test4")

        self.assertIsNotNone(graph.root.children[0].children[0].children[0].children[0].children)
        self.assertEqual(len(graph.root.children[0].children[0].children[0].children[0].children), 1)
        self.assertIsInstance(graph.root.children[0].children[0].children[0].children[0].children[0], PatternBotNode)
        self.assertEqual(graph.root.children[0].children[0].children[0].children[0].children[0].word, "bot1")

        self.assertIsNotNone(graph.root.children[0].children[0].children[0].children[0].children[0].children)
        self.assertEqual(len(graph.root.children[0].children[0].children[0].children[0].children[0].children), 1)
        self.assertIsInstance(graph.root.children[0].children[0].children[0].children[0].children[0].children[0],
                              PatternWordNode)
        self.assertEqual(graph.root.children[0].children[0].children[0].children[0].children[0].children[0].word,
                         "test6")

    def test_add_pattern_to_graph_basic_zero_or_more(self):
        graph = PatternGraph()
        topic_element = ET.fromstring('<topic>*</topic>')
        that_element = ET.fromstring('<that>*</that>')
        template_graph_root = None

        element = ET.fromstring('<pattern>#</pattern>')
        graph.add_pattern_to_graph(element, topic_element, that_element, template_graph_root)

    def test_add_pattern_to_graph_zero_or_more_front(self):
        graph = PatternGraph()
        topic_element = ET.fromstring('<topic>*</topic>')
        that_element = ET.fromstring('<that>*</that>')
        template_graph_root = None

        element = ET.fromstring('<pattern># XXX</pattern>')
        graph.add_pattern_to_graph(element, topic_element, that_element, template_graph_root)

    def test_add_pattern_to_graph_zero_or_more_middle(self):
        graph = PatternGraph()
        topic_element = ET.fromstring('<topic>*</topic>')
        that_element = ET.fromstring('<that>*</that>')
        template_graph_root = None

        element = ET.fromstring('<pattern>XXX # YYY</pattern>')
        graph.add_pattern_to_graph(element, topic_element, that_element, template_graph_root)

    def test_add_pattern_to_graph_zero_or_more_last(self):
        graph = PatternGraph()
        topic_element = ET.fromstring('<topic>*</topic>')
        that_element = ET.fromstring('<that>*</that>')
        template_graph_root = None

        element = ET.fromstring('<pattern>XXX #</pattern>')
        graph.add_pattern_to_graph(element, topic_element, that_element, template_graph_root)

    def test_add_pattern_to_graph_zero_or_more_multiple(self):
        graph = PatternGraph()
        topic_element = ET.fromstring('<topic>*</topic>')
        that_element = ET.fromstring('<that>*</that>')
        template_graph_root = None

        element = ET.fromstring('<pattern>XXX # YYY # ZZZ</pattern>')
        graph.add_pattern_to_graph(element, topic_element, that_element, template_graph_root)

    def test_add_pattern_to_graph_basic_zero_or_more_with_patterns(self):
        graph = PatternGraph()
        topic_element = ET.fromstring('<topic>*</topic>')
        that_element = ET.fromstring('<that>*</that>')

        element = ET.fromstring('<pattern># HELLO</pattern>')
        template_graph_root = TemplateWordNode("RESPONSE1")
        graph.add_pattern_to_graph(element, topic_element, that_element, template_graph_root)

        element = ET.fromstring('<pattern>WELL HI THERE</pattern>')
        template_graph_root = TemplateWordNode("RESPONSE2")
        graph.add_pattern_to_graph(element, topic_element, that_element, template_graph_root)

    def test_add_pattern_to_graph_basic_one_or_more(self):
        graph = PatternGraph()
        topic_element = ET.fromstring('<topic>*</topic>')
        that_element = ET.fromstring('<that>*</that>')
        template_graph_root = None

        element = ET.fromstring('<pattern>*</pattern>')
        graph.add_pattern_to_graph(element, topic_element, that_element, template_graph_root)
        
        self.assertIsNotNone(graph.root)
        self.assertIsNotNone(graph.root._1ormore_star)
        self.assertIsInstance(graph.root._1ormore_star, PatternOneOrMoreWildCardNode)
        self.assertEqual(graph.root._1ormore_star.wildcard, "*")

        self.assertEqual(len(graph.root._priority_words), 0)
        self.assertIsNone(graph.root._0ormore_arrow)
        self.assertIsNone(graph.root._0ormore_hash)
        self.assertIsNone(graph.root._1ormore_underline)

    def test_add_pattern_to_graph_one_or_more_front(self):
        graph = PatternGraph()
        topic_element = ET.fromstring('<topic>*</topic>')
        that_element = ET.fromstring('<that>*</that>')
        template_graph_root = None

        element = ET.fromstring('<pattern>* XXX</pattern>')
        graph.add_pattern_to_graph(element, topic_element, that_element, template_graph_root)

    def test_add_pattern_to_graph_one_or_more_middle(self):
        graph = PatternGraph()
        topic_element = ET.fromstring('<topic>*</topic>')
        that_element = ET.fromstring('<that>*</that>')
        template_graph_root = None

        element = ET.fromstring('<pattern>XXX * YYY</pattern>')
        graph.add_pattern_to_graph(element, topic_element, that_element, template_graph_root)

    def test_add_pattern_to_graph_one_or_more_last(self):
        graph = PatternGraph()
        topic_element = ET.fromstring('<topic>*</topic>')
        that_element = ET.fromstring('<that>*</that>')
        template_graph_root = None

        element = ET.fromstring('<pattern>XXX *</pattern>')
        graph.add_pattern_to_graph(element, topic_element, that_element, template_graph_root)

    ##################################################################################################################
    #
        
    def test_add_topic_to_node_star(self):
        graph = PatternGraph()

        base_node = PatternWordNode("TOPIC_TEST")

        topic_element = ET.fromstring('<topic>*</topic>')

        end_node = graph.add_topic_to_node(topic_element, base_node)
        self.assertIsNotNone(end_node)

        self.assertIsNotNone(base_node)
        self.assertIsNotNone(base_node.topic)
        self.assertIsInstance(base_node.topic, PatternTopicNode)

        self.assertFalse(base_node.topic.has_children())
        self.assertTrue(base_node.topic.has_wildcard())
        self.assertIsNotNone(base_node.topic.star)
        self.assertEqual(base_node.topic.star.wildcard, "*")

    def test_add_topic_to_node_pattern(self):
        graph = PatternGraph()

        base_node = PatternWordNode("TOPIC_TEST")

        topic_element = ET.fromstring('<topic>HELLO WORLD</topic>')

        end_node = graph.add_topic_to_node(topic_element, base_node)
        self.assertIsNotNone(end_node)

        self.assertIsNotNone(base_node)
        self.assertIsNotNone(base_node.topic)
        self.assertIsInstance(base_node.topic, PatternTopicNode)

        self.assertTrue(base_node.topic.has_children())
        self.assertIsInstance(base_node.topic.children[0], PatternWordNode)
        self.assertEqual(base_node.topic.children[0].word, "HELLO")

        self.assertTrue(base_node.topic.children[0].has_children())
        self.assertIsInstance(base_node.topic.children[0].children[0], PatternWordNode)
        self.assertEqual(base_node.topic.children[0].children[0].word, "WORLD")

    def test_add_topic_to_node_pattern_with_set(self):
        graph = PatternGraph()

        base_node = PatternWordNode("TOPIC_TEST")

        topic_element = ET.fromstring('<topic>HELLO <set name="test" /> WORLD</topic>')

        end_node = graph.add_topic_to_node(topic_element, base_node)
        self.assertIsNotNone(end_node)

        self.assertIsNotNone(base_node)
        self.assertIsNotNone(base_node.topic)
        self.assertIsInstance(base_node.topic, PatternTopicNode)

        self.assertTrue(base_node.topic.has_children())
        self.assertIsInstance(base_node.topic.children[0], PatternWordNode)
        self.assertEqual(base_node.topic.children[0].word, "HELLO")

        self.assertTrue(base_node.topic.children[0].has_children())
        self.assertIsInstance(base_node.topic.children[0].children[0], PatternSetNode)
        self.assertEqual(base_node.topic.children[0].children[0].word, "TEST")

        self.assertTrue(base_node.topic.children[0].children[0].has_children())
        self.assertIsInstance(base_node.topic.children[0].children[0].children[0], PatternWordNode)
        self.assertEqual(base_node.topic.children[0].children[0].children[0].word, "WORLD")

    ##################################################################################################################
    #

    def test_add_that_to_node_star(self):
        graph = PatternGraph()

        base_node = PatternWordNode("THAT_TEST")

        that_element = ET.fromstring('<that>*</that>')

        end_node = graph.add_that_to_node(that_element, base_node)
        self.assertIsNotNone(end_node)

        self.assertIsNotNone(base_node)
        self.assertIsNotNone(base_node.that)
        self.assertIsInstance(base_node.that, PatternThatNode)

        self.assertFalse(base_node.that.has_children())
        self.assertTrue(base_node.that.has_wildcard())
        self.assertIsNotNone(base_node.that.star)
        self.assertEqual(base_node.that.star.wildcard, "*")

    def test_add_that_to_node_pattern(self):
        graph = PatternGraph()

        base_node = PatternWordNode("THAT_TEST")

        that_element = ET.fromstring('<that>HELLO WORLD</that>')

        end_node = graph.add_that_to_node(that_element, base_node)
        self.assertIsNotNone(end_node)

        self.assertIsNotNone(base_node)
        self.assertIsNotNone(base_node.that)
        self.assertIsInstance(base_node.that, PatternThatNode)

        self.assertTrue(base_node.that.has_children())
        self.assertIsInstance(base_node.that.children[0], PatternWordNode)
        self.assertEqual(base_node.that.children[0].word, "HELLO")

        self.assertTrue(base_node.that.children[0].has_children())
        self.assertIsInstance(base_node.that.children[0].children[0], PatternWordNode)
        self.assertEqual(base_node.that.children[0].children[0].word, "WORLD")

    def test_add_that_to_node_pattern_with_set(self):
        graph = PatternGraph()

        base_node = PatternWordNode("THAT_TEST")

        that_element = ET.fromstring('<that>HELLO <set name="test" /> WORLD</that>')

        end_node = graph.add_that_to_node(that_element, base_node)
        self.assertIsNotNone(end_node)

        self.assertIsNotNone(base_node)
        self.assertIsNotNone(base_node.that)
        self.assertIsInstance(base_node.that, PatternThatNode)

        self.assertTrue(base_node.that.has_children())
        self.assertIsInstance(base_node.that.children[0], PatternWordNode)
        self.assertEqual(base_node.that.children[0].word, "HELLO")

        self.assertTrue(base_node.that.children[0].has_children())
        self.assertIsInstance(base_node.that.children[0].children[0], PatternSetNode)
        self.assertEqual(base_node.that.children[0].children[0].word, "TEST")

        self.assertTrue(base_node.that.children[0].children[0].has_children())
        self.assertIsInstance(base_node.that.children[0].children[0].children[0], PatternWordNode)
        self.assertEqual(base_node.that.children[0].children[0].children[0].word, "WORLD")


    ##################################################################################################################
    #

    def test_add_pattern_with_diff_topics_to_graph(self):
        graph = PatternGraph()

        topic_element = ET.fromstring('<topic>*</topic>')
        that_element = ET.fromstring('<that>*</that>')
        template_graph_root = None
        element = ET.fromstring("<pattern>test1</pattern>")
        graph.add_pattern_to_graph(element, topic_element, that_element, template_graph_root)

        topic_element = ET.fromstring('<topic>topic1</topic>')
        that_element = ET.fromstring('<that>that1</that>')
        template_graph_root = None
        element = ET.fromstring("<pattern>test1</pattern>")
        graph.add_pattern_to_graph(element, topic_element, that_element, template_graph_root)

    ##################################################################################################################
    #

    def test_simple_hash_and_star_at_end(self):
        graph = PatternGraph()

        pattern_element = ET.fromstring("<pattern>A # *</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        self.assertIsNotNone(graph.root)
        self.assertIsNotNone(graph.root.children)
        self.assertEqual(len(graph.root.children), 1)

        word_node = graph.root.children[0]
        self.assertIsInstance(word_node, PatternWordNode)
        self.assertEqual(word_node.word, "A")

        self.assertTrue(word_node.has_zero_or_more())
        if word_node.arrow is not None:
            wildcard_node = word_node.arrow
        elif word_node.hash is not None:
            wildcard_node = word_node.hash
        self.assertIsNotNone(wildcard_node)

        self.assertTrue(wildcard_node.has_one_or_more())
        if word_node.star is not None:
            wildcard_node = word_node.star
        elif word_node.underline is not None:
            wildcard_node = word_node.underline
        self.assertIsNotNone(wildcard_node)

import xml.etree.ElementTree as ET

from programytest.parser.base import ParserTestsBaseClass

from programy.parser.exceptions import ParserException
from programy.parser.pattern.graph import PatternGraph
from programy.parser.pattern.nodes.root import PatternRootNode
from programy.parser.pattern.nodes.topic import PatternTopicNode
from programy.parser.pattern.nodes.that import PatternThatNode
from programy.parser.pattern.nodes.word import PatternWordNode
from programy.parser.pattern.nodes.priority import PatternPriorityWordNode
from programy.parser.pattern.nodes.oneormore import PatternOneOrMoreWildCardNode
from programy.parser.pattern.nodes.zeroormore import PatternZeroOrMoreWildCardNode
from programy.parser.pattern.nodes.template import PatternTemplateNode
from programy.parser.pattern.nodes.iset import PatternISetNode
from programy.parser.pattern.nodes.set import PatternSetNode
from programy.parser.pattern.nodes.bot import PatternBotNode
from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.word import TemplateWordNode


class PatternGraphTests(ParserTestsBaseClass):

    def test_init_no_root(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        self.assertIsNotNone(graph)
        self.assertIsNotNone(graph.root)
        self.assertIsInstance(graph.root, PatternRootNode)

    def test_init_with_root(self):
        root = PatternRootNode()
        graph = PatternGraph(self._client_context.brain.aiml_parser, root_node=root)
        self.assertIsNotNone(graph)
        self.assertIsNotNone(graph.root)
        self.assertIsInstance(graph.root, PatternRootNode)
        self.assertEqual(graph.root, root)

    def test_init_with_invalid_root(self):
        root = PatternWordNode("Word")
        with self.assertRaises(ParserException):
            graph = PatternGraph(self._client_context.brain.aiml_parser, root_node=root)

    def test_node_from_text_prioity(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        node = graph.node_from_text("$A")
        self.assertIsNotNone(node)
        self.assertIsInstance(node, PatternPriorityWordNode)

    def test_node_from_text_zeroormore(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        node = graph.node_from_text("^")
        self.assertIsNotNone(node)
        self.assertIsInstance(node, PatternZeroOrMoreWildCardNode)

        node = graph.node_from_text("#")
        self.assertIsNotNone(node)
        self.assertIsInstance(node, PatternZeroOrMoreWildCardNode)

    def test_node_from_text_oneormore(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        node = graph.node_from_text("_")
        self.assertIsNotNone(node)
        self.assertIsInstance(node, PatternOneOrMoreWildCardNode)

        node = graph.node_from_text("*")
        self.assertIsNotNone(node)
        self.assertIsInstance(node, PatternOneOrMoreWildCardNode)

    def test_node_from_text_word(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        node = graph.node_from_text("X")
        self.assertIsNotNone(node)
        self.assertIsInstance(node, PatternWordNode)

    def test_node_from_element_iset(self):
        set_element = ET.fromstring('<iset>yes, no</iset>')
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        node = graph.node_from_element(set_element)
        self.assertIsNotNone(node)
        self.assertIsInstance(node, PatternISetNode)

    def test_node_from_element_set(self):
        set_element = ET.fromstring('<set>colour</set>')
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        node = graph.node_from_element(set_element)
        self.assertIsNotNone(node)
        self.assertIsInstance(node, PatternSetNode)

    def test_node_from_element_bot(self):
        bot_element = ET.fromstring('<bot>name</bot>')
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        node = graph.node_from_element(bot_element)
        self.assertIsNotNone(node)
        self.assertIsInstance(node, PatternBotNode)

    def test_parse_text_nothing(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        root = PatternRootNode()
        final_node = graph._parse_text("", root)
        self.assertIsNotNone(final_node)
        self.assertIsInstance(final_node, PatternRootNode)
        self.assertEqual(final_node, root)

    def test_parse_text_word(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        root = PatternRootNode()
        final_node = graph._parse_text("HELLO", root)
        self.assertIsNotNone(final_node)
        self.assertIsInstance(final_node, PatternWordNode)
        self.assertEqual(final_node.word, "HELLO")

    def test_parse_text_multiple_words(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        root = PatternRootNode()
        final_node = graph._parse_text("HELLO THERE", root)
        self.assertIsNotNone(final_node)
        self.assertIsInstance(final_node, PatternWordNode)
        self.assertEqual(final_node.word, "THERE")

    def test_parse_text_multiple_words_whitespaces(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        root = PatternRootNode()
        final_node = graph._parse_text("HELLO \t\n\r THERE", root)
        self.assertIsNotNone(final_node)
        self.assertIsInstance(final_node, PatternWordNode)
        self.assertEqual(final_node.word, "THERE")

    def test_parse_text_priority(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        root = PatternRootNode()
        final_node = graph._parse_text("$HELLO", root)
        self.assertIsNotNone(final_node)
        self.assertIsInstance(final_node, PatternPriorityWordNode)

    def test_parse_text_zeroormore(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        root = PatternRootNode()
        final_node = graph._parse_text("^", root)
        self.assertIsNotNone(final_node)
        self.assertIsInstance(final_node, PatternZeroOrMoreWildCardNode)

        final_node = graph._parse_text("#", root)
        self.assertIsNotNone(final_node)
        self.assertIsInstance(final_node, PatternZeroOrMoreWildCardNode)

    def test_parse_text_oneormore(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        root = PatternRootNode()
        final_node = graph._parse_text("_", root)
        self.assertIsNotNone(final_node)
        self.assertIsInstance(final_node, PatternOneOrMoreWildCardNode)

        final_node = graph._parse_text("*", root)
        self.assertIsNotNone(final_node)
        self.assertIsInstance(final_node, PatternOneOrMoreWildCardNode)

    def get_text_from_element_word(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        set_element = ET.fromstring('<set>colour</set>')
        text = graph.get_text_from_element(set_element)
        self.assertIsNotNone(text)
        self.assertEqual("colour", text)

    def get_text_from_element_whitespaces(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        set_element = ET.fromstring('<set>colour \n\r\t  eyes</set>')
        text = graph.get_text_from_element(set_element)
        self.assertIsNotNone(text)
        self.assertEqual("colour set", text)

    def get_tail_from_element_word(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        set_element = ET.fromstring('<set>colour</set>this')
        text = graph.get_tail_from_element(set_element)
        self.assertIsNotNone(text)
        self.assertEqual("this", text)

    def get_tail_from_element_word_whitespaces(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        set_element = ET.fromstring('<set>colour</set>this \t that \n the \r other')
        text = graph.get_tail_from_element(set_element)
        self.assertIsNotNone(text)
        self.assertEqual("this that the other", text)

    def test_add_pattern_to_node(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        pattern = ET.fromstring('<pattern>HELLO</pattern>')
        node = graph.add_pattern_to_node(pattern)
        self.assertIsNotNone(node)
        self.assertIsInstance(node, PatternWordNode)
        self.assertEqual(node.word, "HELLO")

    def test_add_pattern_to_node_whitespaces(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        pattern = ET.fromstring("""
        <pattern>
            HELLO
        </pattern>""")
        node = graph.add_pattern_to_node(pattern)
        self.assertIsNotNone(node)
        self.assertIsInstance(node, PatternWordNode)
        self.assertEqual(node.word, "HELLO")

    def test_add_topic_to_node_word(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        pattern = ET.fromstring("""
        <pattern>
            HELLO
        </pattern>""")
        pattern_node = graph.add_pattern_to_node(pattern)

        topic = ET.fromstring("""
        <topic>
            THERE
        </topic>""")
        topic_node = graph.add_that_to_node(topic, pattern_node)
        self.assertIsNotNone(topic_node)
        self.assertIsInstance(topic_node, PatternWordNode)
        self.assertEqual(topic_node.word, "THERE")

    def test_add_topic_to_node_wildcard(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        pattern = ET.fromstring("""
        <pattern>
            HELLO
        </pattern>""")
        pattern_node = graph.add_pattern_to_node(pattern)

        topic = ET.fromstring("""
        <topic>
            *
        </topic>""")
        topic_node = graph.add_that_to_node(topic, pattern_node)
        self.assertIsNotNone(topic_node)
        self.assertIsInstance(topic_node, PatternOneOrMoreWildCardNode)
        self.assertEqual(topic_node.wildcard, "*")

    def test_add_that_to_node_word(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        pattern = ET.fromstring("""
        <pattern>
            HELLO
        </pattern>""")
        pattern_node = graph.add_pattern_to_node(pattern)

        topic = ET.fromstring("""
        <topic>
            THERE
        </topic>""")
        topic_node = graph.add_that_to_node(topic, pattern_node)

        that = ET.fromstring("""
        <that>
            HERE
        </that>""")
        that_node = graph.add_that_to_node(that, topic_node)
        self.assertIsNotNone(that_node)
        self.assertIsInstance(that_node, PatternWordNode)
        self.assertEqual(that_node.word, "HERE")

    def test_add_that_to_node_word(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        pattern = ET.fromstring("""
        <pattern>
            HELLO
        </pattern>""")
        pattern_node = graph.add_pattern_to_node(pattern)

        topic = ET.fromstring("""
        <topic>
            THERE
        </topic>""")
        topic_node = graph.add_that_to_node(topic, pattern_node)

        that = ET.fromstring("""
        <that>
            *
        </that>""")
        that_node = graph.add_that_to_node(that, topic_node)
        self.assertIsNotNone(that_node)
        self.assertIsInstance(that_node, PatternOneOrMoreWildCardNode)
        self.assertEqual(that_node.wildcard, "*")

    def test_add_template_to_node(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        pattern = ET.fromstring("""
        <pattern>
            HELLO
        </pattern>""")
        pattern_node = graph.add_pattern_to_node(pattern)

        topic = ET.fromstring("""
        <topic>
            THERE
        </topic>""")
        topic_node = graph.add_that_to_node(topic, pattern_node)

        that = ET.fromstring("""
        <that>
            *
        </that>""")
        that_node = graph.add_that_to_node(that, topic_node)

        template = TemplateWordNode("TEST")
        template_node = graph.add_template_to_node(template, that_node)
        self.assertIsNotNone(template_node)
        self.assertIsInstance(template_node, PatternTemplateNode)

    def test_add_pattern_to_graph(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        pattern = ET.fromstring("<pattern>HELLO</pattern>")
        topic = ET.fromstring("<topic>HELLO</topic>")
        that = ET.fromstring("<that>HELLO</that>")
        template = TemplateWordNode("TEST")
        graph.add_pattern_to_graph(pattern, topic, that, template)

        self.assertIsNotNone(graph.root)
        self.assertIsNotNone(graph.root.child(0))
        self.assertIsNotNone(graph.root.child(0).topic)
        self.assertIsNotNone(graph.root.child(0).topic.child(0))
        self.assertIsNotNone(graph.root.child(0).topic.child(0).that)
        self.assertIsNotNone(graph.root.child(0).topic.child(0).that.child(0))
        self.assertIsNotNone(graph.root.child(0).topic.child(0).that.child(0).template)

    def test_count_word_in_patterns(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        count = graph.count_words_in_patterns()
        self.assertEqual(0, count)
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        pattern = ET.fromstring("<pattern>HELLO</pattern>")
        topic = ET.fromstring("<topic>HELLO</topic>")
        that = ET.fromstring("<that>HELLO</that>")
        template = TemplateWordNode("TEST")
        graph.add_pattern_to_graph(pattern, topic, that, template)

        count = graph.count_words_in_patterns()
        self.assertEqual(1, count)

    def test_count_words_in_patterns(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        count = graph.count_words_in_patterns()
        self.assertEqual(0, count)
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        pattern1 = ET.fromstring("<pattern>HELLO THErE</pattern>")
        topic = ET.fromstring("<topic>HELLO</topic>")
        that = ET.fromstring("<that>HELLO</that>")
        template = TemplateWordNode("TEST")

        graph.add_pattern_to_graph(pattern1, topic, that, template)
        count = graph.count_words_in_patterns()
        self.assertEqual(2, count)

        pattern2 = ET.fromstring("<pattern>WHERE ARE YOU</pattern>")
        graph.add_pattern_to_graph(pattern2, topic, that, template)
        count = graph.count_words_in_patterns()
        self.assertEqual(5, count)

    def test_add_pattern_with_whitepsace(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
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
        graph = PatternGraph(self._client_context.brain.aiml_parser)
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
        self.assertEqual(graph.root.children[0].word, "test2")
        self.assertIsInstance(graph.root.children[0], PatternWordNode)
        self.assertEqual(graph.root.children[1].word, "test1")

    def test_add_pattern_to_graph_multi_word(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
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
        self.assertEqual(graph.root.children[0].children[0].word, "test3")
        self.assertEqual(len(graph.root.children[0].children[0].children), 1)
        self.assertIsInstance(graph.root.children[0].children[0].children[0], PatternWordNode)
        self.assertEqual(graph.root.children[0].children[0].children[0].word, "test4")

        self.assertIsInstance(graph.root.children[0].children[1], PatternWordNode)
        self.assertEqual(graph.root.children[0].children[1].word, "test2")

    def test_add_pattern_to_graph_basic_set_text(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        topic_element = ET.fromstring('<topic>*</topic>')
        that_element = ET.fromstring('<that>*</that>')
        template_graph_root = None

        self._client_context.brain.sets._sets["SET1"] = ["VAL1", "VAL2", "VAL3", "VAL5"]

        element = ET.fromstring('<pattern><set>set1</set> IS A VALUE</pattern>')
        graph.add_pattern_to_graph(element, topic_element, that_element, template_graph_root)

        self.assertIsNotNone(graph.root)
        self.assertIsNotNone(graph.root.children)
        self.assertEqual(len(graph.root.children), 1)
        self.assertIsInstance(graph.root.children[0], PatternSetNode)
        self.assertEqual(graph.root.children[0].set_name, "SET1")

    def test_add_pattern_to_graph_basic_set_name_attrib(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        topic_element = ET.fromstring('<topic>*</topic>')
        that_element = ET.fromstring('<that>*</that>')
        template_graph_root = None

        self._client_context.brain.sets._sets["SET1"] = ["val1", "val2", "val3", "val5"]

        element = ET.fromstring('<pattern><set name="set1" /></pattern>')
        graph.add_pattern_to_graph(element, topic_element, that_element, template_graph_root)

        self.assertIsNotNone(graph.root)
        self.assertIsNotNone(graph.root.children)
        self.assertEqual(len(graph.root.children), 1)
        self.assertIsInstance(graph.root.children[0], PatternSetNode)
        self.assertEqual(graph.root.children[0].set_name, "SET1")

    def test_add_pattern_to_graph_basic_iset(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        topic_element = ET.fromstring('<topic>*</topic>')
        that_element = ET.fromstring('<that>*</that>')
        template_graph_root = None

        element = ET.fromstring('<pattern><iset>word1, word2, word3</iset> A VALUE</pattern>')
        graph.add_pattern_to_graph(element, topic_element, that_element, template_graph_root)

        self.assertIsNotNone(graph.root)
        self.assertIsNotNone(graph.root.children)
        self.assertEqual(len(graph.root.children), 1)
        self.assertIsInstance(graph.root.children[0], PatternISetNode)

    def test_add_pattern_to_graph_basic_multiple_isets(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        topic_element = ET.fromstring('<topic>*</topic>')
        that_element = ET.fromstring('<that>*</that>')
        template_graph_root = None

        element1 = ET.fromstring('<pattern>IS <iset>word1, word2, word3</iset> A VALUE</pattern>')
        graph.add_pattern_to_graph(element1, topic_element, that_element, template_graph_root)
        element2 = ET.fromstring('<pattern>IS <iset>word1, word2, word3</iset> A ANOTHER VALUE</pattern>')
        graph.add_pattern_to_graph(element2, topic_element, that_element, template_graph_root)

        self.assertIsNotNone(graph.root)
        self.assertIsNotNone(graph.root.children)
        self.assertEqual(len(graph.root.children), 1)
        self.assertIsInstance(graph.root.children[0], PatternWordNode)
        self.assertEqual(len(graph.root.children[0].children), 1)
        self.assertIsInstance(graph.root.children[0].children[0], PatternISetNode)

    def test_add_pattern_to_graph_basic_bot_text(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        topic_element = ET.fromstring('<topic>*</topic>')
        that_element = ET.fromstring('<that>*</that>')
        template_graph_root = None

        self._client_context.brain.properties.add_property('bot1', 'val1')

        element = ET.fromstring('<pattern><bot>bot1</bot></pattern>')
        graph.add_pattern_to_graph(element, topic_element, that_element, template_graph_root)

        self.assertIsNotNone(graph.root)
        self.assertIsNotNone(graph.root.children)
        self.assertEqual(len(graph.root.children), 1)
        self.assertIsInstance(graph.root.children[0], PatternBotNode)
        self.assertEqual(graph.root.children[0].property, "bot1")

    def test_add_pattern_to_graph_basic_bot_name_attrib(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        topic_element = ET.fromstring('<topic>*</topic>')
        that_element = ET.fromstring('<that>*</that>')
        template_graph_root = None

        self._client_context.brain.properties.add_property('bot1', 'val1')

        element = ET.fromstring('<pattern><bot name="bot1" /></pattern>')
        graph.add_pattern_to_graph(element, topic_element, that_element, template_graph_root)

        self.assertIsNotNone(graph.root)
        self.assertIsNotNone(graph.root.children)
        self.assertEqual(len(graph.root.children), 1)
        self.assertIsInstance(graph.root.children[0], PatternBotNode)
        self.assertEqual(graph.root.children[0].property, "bot1")

    def test_add_pattern_to_graph_word_set_bot(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        topic_element = ET.fromstring('<topic>*</topic>')
        that_element = ET.fromstring('<that>*</that>')
        template_graph_root = None

        self._client_context.brain.sets._sets["SET1"] = ["val1", "val2", "val3", "val5"]
        self._client_context.brain.properties.add_property('bot1', 'val1')

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
        self.assertEqual(graph.root.children[0].children[0].children[0].set_name, "SET1")

        self.assertIsNotNone(graph.root.children[0].children[0].children[0].children)
        self.assertEqual(len(graph.root.children[0].children[0].children[0].children), 1)
        self.assertIsInstance(graph.root.children[0].children[0].children[0].children[0], PatternWordNode)
        self.assertEqual(graph.root.children[0].children[0].children[0].children[0].word, "test4")

        self.assertIsNotNone(graph.root.children[0].children[0].children[0].children[0].children)
        self.assertEqual(len(graph.root.children[0].children[0].children[0].children[0].children), 1)
        self.assertIsInstance(graph.root.children[0].children[0].children[0].children[0].children[0], PatternBotNode)
        self.assertEqual(graph.root.children[0].children[0].children[0].children[0].children[0].property, "bot1")

        self.assertIsNotNone(graph.root.children[0].children[0].children[0].children[0].children[0].children)
        self.assertEqual(len(graph.root.children[0].children[0].children[0].children[0].children[0].children), 1)
        self.assertIsInstance(graph.root.children[0].children[0].children[0].children[0].children[0].children[0],
                              PatternWordNode)
        self.assertEqual(graph.root.children[0].children[0].children[0].children[0].children[0].children[0].word,
                         "test6")

    def test_add_pattern_to_graph_basic_zero_or_more(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        topic_element = ET.fromstring('<topic>*</topic>')
        that_element = ET.fromstring('<that>*</that>')
        template_graph_root = None

        element = ET.fromstring('<pattern>#</pattern>')
        graph.add_pattern_to_graph(element, topic_element, that_element, template_graph_root)

    def test_add_pattern_to_graph_zero_or_more_front(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        topic_element = ET.fromstring('<topic>*</topic>')
        that_element = ET.fromstring('<that>*</that>')
        template_graph_root = None

        element = ET.fromstring('<pattern># XXX</pattern>')
        graph.add_pattern_to_graph(element, topic_element, that_element, template_graph_root)

    def test_add_pattern_to_graph_zero_or_more_middle(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        topic_element = ET.fromstring('<topic>*</topic>')
        that_element = ET.fromstring('<that>*</that>')
        template_graph_root = None

        element = ET.fromstring('<pattern>XXX # YYY</pattern>')
        graph.add_pattern_to_graph(element, topic_element, that_element, template_graph_root)

    def test_add_pattern_to_graph_zero_or_more_last(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        topic_element = ET.fromstring('<topic>*</topic>')
        that_element = ET.fromstring('<that>*</that>')
        template_graph_root = None

        element = ET.fromstring('<pattern>XXX #</pattern>')
        graph.add_pattern_to_graph(element, topic_element, that_element, template_graph_root)

    def test_add_pattern_to_graph_zero_or_more_multiple(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        topic_element = ET.fromstring('<topic>*</topic>')
        that_element = ET.fromstring('<that>*</that>')
        template_graph_root = None

        element = ET.fromstring('<pattern>XXX # YYY # ZZZ</pattern>')
        graph.add_pattern_to_graph(element, topic_element, that_element, template_graph_root)

    def test_add_pattern_to_graph_basic_zero_or_more_with_patterns(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        topic_element = ET.fromstring('<topic>*</topic>')
        that_element = ET.fromstring('<that>*</that>')

        element = ET.fromstring('<pattern># HELLO</pattern>')
        template_graph_root = TemplateWordNode("RESPONSE1")
        graph.add_pattern_to_graph(element, topic_element, that_element, template_graph_root)

        element = ET.fromstring('<pattern>WELL HI THERE</pattern>')
        template_graph_root = TemplateWordNode("RESPONSE2")
        graph.add_pattern_to_graph(element, topic_element, that_element, template_graph_root)

    def test_add_pattern_to_graph_basic_one_or_more(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
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
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        topic_element = ET.fromstring('<topic>*</topic>')
        that_element = ET.fromstring('<that>*</that>')
        template_graph_root = None

        element = ET.fromstring('<pattern>* XXX</pattern>')
        graph.add_pattern_to_graph(element, topic_element, that_element, template_graph_root)

    def test_add_pattern_to_graph_one_or_more_middle(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        topic_element = ET.fromstring('<topic>*</topic>')
        that_element = ET.fromstring('<that>*</that>')
        template_graph_root = None

        element = ET.fromstring('<pattern>XXX * YYY</pattern>')
        graph.add_pattern_to_graph(element, topic_element, that_element, template_graph_root)

    def test_add_pattern_to_graph_one_or_more_last(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        topic_element = ET.fromstring('<topic>*</topic>')
        that_element = ET.fromstring('<that>*</that>')
        template_graph_root = None

        element = ET.fromstring('<pattern>XXX *</pattern>')
        graph.add_pattern_to_graph(element, topic_element, that_element, template_graph_root)

    ##################################################################################################################
    #

    def test_add_topic_to_node_star(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)

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
        graph = PatternGraph(self._client_context.brain.aiml_parser)

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
        graph = PatternGraph(self._client_context.brain.aiml_parser)

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
        self.assertEqual(base_node.topic.children[0].children[0].set_name, "TEST")

        self.assertTrue(base_node.topic.children[0].children[0].has_children())
        self.assertIsInstance(base_node.topic.children[0].children[0].children[0], PatternWordNode)
        self.assertEqual(base_node.topic.children[0].children[0].children[0].word, "WORLD")

    ##################################################################################################################
    #

    def test_add_that_to_node_star(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)

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
        graph = PatternGraph(self._client_context.brain.aiml_parser)

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
        graph = PatternGraph(self._client_context.brain.aiml_parser)

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
        self.assertEqual(base_node.that.children[0].children[0].set_name, "TEST")

        self.assertTrue(base_node.that.children[0].children[0].has_children())
        self.assertIsInstance(base_node.that.children[0].children[0].children[0], PatternWordNode)
        self.assertEqual(base_node.that.children[0].children[0].children[0].word, "WORLD")


    ##################################################################################################################
    #

    def test_add_pattern_with_diff_topics_to_graph(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)

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
        graph = PatternGraph(self._client_context.brain.aiml_parser)

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

    ##################################################################################################################
    #

    def test_duplicates(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        topic_element = ET.fromstring('<topic>*</topic>')
        that_element = ET.fromstring('<that>*</that>')
        template_graph_root = None

        pattern1 = "<pattern>IS A</pattern>"
        pattern2 = "<pattern>IS * <set>article</set> *</pattern>"

        element1 = ET.fromstring(pattern1)
        graph.add_pattern_to_graph(element1, topic_element, that_element, template_graph_root)
        element2 = ET.fromstring(pattern2)
        graph.add_pattern_to_graph(element2, topic_element, that_element, template_graph_root)

import xml.etree.ElementTree as ET

from test.parser.pattern.nodes.base import PatternTestBaseClass

from programy.parser.exceptions import ParserException, DuplicateGrammarException
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


class PatternGraphTests(PatternTestBaseClass):

    def test_duplicate_pattern(self):
        graph = PatternGraph()

        pattern_element = ET.fromstring("<pattern>A # *</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        pattern_element = ET.fromstring("<pattern>A # *</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        with self.assertRaises(DuplicateGrammarException):
            graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

    def test_duplicate_pattern_same_topics(self):
        graph = PatternGraph()

        pattern_element = ET.fromstring("<pattern>A # *</pattern>")
        topic_element = ET.fromstring("<topic>X Y</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        pattern_element = ET.fromstring("<pattern>A # *</pattern>")
        topic_element = ET.fromstring("<topic>X Y</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        with self.assertRaises(DuplicateGrammarException):
            graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

    def test_duplicate_pattern_same_thats(self):
        graph = PatternGraph()

        pattern_element = ET.fromstring("<pattern>A # *</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>X Y</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        pattern_element = ET.fromstring("<pattern>A # *</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>X Y</that>")
        template_node = TemplateNode()

        with self.assertRaises(DuplicateGrammarException):
            graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

    def test_duplicate_pattern_different_topics(self):
        graph = PatternGraph()

        pattern_element = ET.fromstring("<pattern>A # *</pattern>")
        topic_element = ET.fromstring("<topic>A B</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        pattern_element = ET.fromstring("<pattern>A # *</pattern>")
        topic_element = ET.fromstring("<topic>X Y</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

    def test_duplicate_pattern_different_thats(self):
        graph = PatternGraph()

        pattern_element = ET.fromstring("<pattern>A # *</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>A B</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        pattern_element = ET.fromstring("<pattern>A # *</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>X Y</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

    def test_duplicate_priority(self):
        graph = PatternGraph()

        pattern_element = ET.fromstring("<pattern>$A</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        pattern_element = ET.fromstring("<pattern>$A</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        with self.assertRaises(DuplicateGrammarException):
            graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

    def test_duplicate_priority_and_word(self):
        graph = PatternGraph()

        pattern_element = ET.fromstring("<pattern>A</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        pattern_element = ET.fromstring("<pattern>$A</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

    def test_duplicate_priority_and_word_otherwayround(self):
        graph = PatternGraph()

        pattern_element = ET.fromstring("<pattern>$A</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        pattern_element = ET.fromstring("<pattern>A</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

    def test_duplicate_set(self):
        graph = PatternGraph()

        pattern_element = ET.fromstring("<pattern><set>A</set></pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        pattern_element = ET.fromstring("<pattern><set>A</set></pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        with self.assertRaises(DuplicateGrammarException):
            graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

    def test_duplicate_set_and_word(self):
        graph = PatternGraph()

        pattern_element = ET.fromstring("<pattern>A</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        pattern_element = ET.fromstring("<pattern><set>A</set></pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

    def test_duplicate_set_and_word_otherwayround(self):
        graph = PatternGraph()

        pattern_element = ET.fromstring("<pattern><set>A</set></pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        pattern_element = ET.fromstring("<pattern>A</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

    def test_duplicate_bot(self):
        graph = PatternGraph()

        pattern_element = ET.fromstring("<pattern><bot>A</bot></pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        pattern_element = ET.fromstring("<pattern><bot>A</bot></pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        with self.assertRaises(DuplicateGrammarException):
            graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

    def test_duplicate_bot_and_word(self):
        graph = PatternGraph()

        pattern_element = ET.fromstring("<pattern>A</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        pattern_element = ET.fromstring("<pattern><bot>A</bot></pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

    def test_duplicate_bot_and_word_otherwayround(self):
        graph = PatternGraph()

        pattern_element = ET.fromstring("<pattern><bot>A</bot></pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        pattern_element = ET.fromstring("<pattern>A</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

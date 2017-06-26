import xml.etree.ElementTree as ET

from test.parser.pattern.base import PatternTestBaseClass

from programy.parser.exceptions import DuplicateGrammarException
from programy.parser.pattern.graph import PatternGraph
from programy.parser.template.nodes.base import TemplateNode


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

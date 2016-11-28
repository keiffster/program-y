import logging
import xml.etree.ElementTree as ET

from programy.dialog import Sentence
from programy.parser.pattern.nodes import *
from programy.parser.pattern.graph import PatternGraph
from programy.parser.pattern.matcher import PatternMatcher
from programy.parser.template.nodes import TemplateNode

from test.parser.pattern.base import PatternTestBaseClass


class PatternMatcherTests(PatternTestBaseClass):

    @classmethod
    def setUpClass(cls):
        PatternMatcherTests.bot = None
        PatternMatcherTests.clientid = "testid"

    def test_simple_sequence(self):

        graph = PatternGraph()

        pattern_element = ET.fromstring("<pattern>A B C</pattern>")
        topic_element =  ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode ()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        matcher = PatternMatcher(graph)

        pattern_stars = []
        topic_stars = []
        that_stars = []
        result = matcher.match(PatternMatcherTests.bot, PatternMatcherTests.clientid,
                               Sentence("A B"), pattern_stars,
                               Sentence("*"), topic_stars,
                               Sentence("*"), that_stars)
        self.assertIsNone(result)
        self.assertEqual(len(pattern_stars), 0)
        self.assertEqual(len(topic_stars), 0)
        self.assertEqual(len(that_stars), 0)

        pattern_stars = []
        topic_stars = []
        that_stars = []
        result = matcher.match(PatternMatcherTests.bot, PatternMatcherTests.clientid,
                               Sentence("A B C D"), pattern_stars,
                               Sentence("*"), topic_stars,
                               Sentence("*"), that_stars)
        self.assertIsNone(result)
        self.assertEqual(len(pattern_stars), 0)
        self.assertEqual(len(topic_stars), 0)
        self.assertEqual(len(that_stars), 0)

        pattern_stars = []
        topic_stars = []
        that_stars = []
        result = matcher.match(PatternMatcherTests.bot, PatternMatcherTests.clientid,
                               Sentence("A B C"), pattern_stars,
                               Sentence("*"), topic_stars,
                               Sentence("*"), that_stars)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, PatternTemplateNode)
        self.assertEqual(len(pattern_stars), 0)
        self.assertEqual(len(topic_stars), 0)
        self.assertEqual(len(that_stars), 0)

        pattern_stars = []
        topic_stars = []
        that_stars = []
        result = matcher.match(PatternMatcherTests.bot, PatternMatcherTests.clientid,
                               Sentence("A B C"), pattern_stars,
                               Sentence("X X"), topic_stars,
                               Sentence("*"), that_stars)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, PatternTemplateNode)
        self.assertEqual(len(pattern_stars), 0)
        self.assertEqual(len(topic_stars), 1)
        self.assertEqual(topic_stars[0], "X X")
        self.assertEqual(len(that_stars), 0)

        pattern_stars = []
        topic_stars = []
        that_stars = []
        result = matcher.match(PatternMatcherTests.bot, PatternMatcherTests.clientid,
                               Sentence("A B C"), pattern_stars,
                               Sentence("*"), topic_stars,
                               Sentence("Y Y"), that_stars)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, PatternTemplateNode)
        self.assertEqual(len(pattern_stars), 0)
        self.assertEqual(len(topic_stars), 0)
        self.assertEqual(len(that_stars), 1)
        self.assertEqual(that_stars[0], "Y Y")

        pattern_stars = []
        topic_stars = []
        that_stars = []
        result = matcher.match(PatternMatcherTests.bot, PatternMatcherTests.clientid,
                               Sentence("A B C"), pattern_stars,
                               Sentence("X X"), topic_stars,
                               Sentence("Y Y"), that_stars)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, PatternTemplateNode)
        self.assertEqual(len(pattern_stars), 0)
        self.assertEqual(len(topic_stars), 1)
        self.assertEqual(topic_stars[0], "X X")
        self.assertEqual(len(that_stars), 1)
        self.assertEqual(that_stars[0], "Y Y")

    def test_simple_star(self):
        graph = PatternGraph()

        pattern_element = ET.fromstring("<pattern>A * C</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        matcher = PatternMatcher(graph)

        pattern_stars = []
        topic_stars = []
        that_stars = []
        result = matcher.match(PatternMatcherTests.bot, PatternMatcherTests.clientid,
                               Sentence("A B B B C"), pattern_stars,
                               Sentence("*"), topic_stars,
                               Sentence("*"), that_stars)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, PatternTemplateNode)
        self.assertEqual(len(pattern_stars), 1)
        self.assertEqual(pattern_stars[0], "B B B")
        self.assertEqual(len(topic_stars), 0)
        self.assertEqual(len(that_stars), 0)

        pattern_stars = []
        topic_stars = []
        that_stars = []
        result = matcher.match(PatternMatcherTests.bot, PatternMatcherTests.clientid,
                               Sentence("A C"), pattern_stars,
                               Sentence("*"), topic_stars,
                               Sentence("*"), that_stars)
        self.assertIsNone(result)
        self.assertEqual(len(pattern_stars), 0)
        self.assertEqual(len(topic_stars), 0)
        self.assertEqual(len(that_stars), 0)

    def test_simple_star_at_front(self):
        graph = PatternGraph()

        pattern_element = ET.fromstring("<pattern>* B C</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        matcher = PatternMatcher(graph)

        pattern_stars = []
        topic_stars = []
        that_stars = []
        result = matcher.match(PatternMatcherTests.bot, PatternMatcherTests.clientid,
                               Sentence("A B C"), pattern_stars,
                               Sentence("*"), topic_stars,
                               Sentence("*"), that_stars)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, PatternTemplateNode)
        self.assertEqual(len(pattern_stars), 1)
        self.assertEqual('A', pattern_stars[0])
        self.assertEqual(len(topic_stars), 0)
        self.assertEqual(len(that_stars), 0)

    def test_simple_star_at_end(self):
        graph = PatternGraph()

        pattern_element = ET.fromstring("<pattern>A B *</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        matcher = PatternMatcher(graph)

        pattern_stars = []
        topic_stars = []
        that_stars = []
        result = matcher.match(PatternMatcherTests.bot, PatternMatcherTests.clientid,
                               Sentence("A B C"), pattern_stars,
                               Sentence("*"), topic_stars,
                               Sentence("*"), that_stars)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, PatternTemplateNode)
        self.assertEqual(len(pattern_stars), 1)
        self.assertEqual('C', pattern_stars[0])
        self.assertEqual(len(topic_stars), 0)
        self.assertEqual(len(that_stars), 0)

    def test_simple_multiple_stars(self):
        graph = PatternGraph()

        pattern_element = ET.fromstring("<pattern>A * * D</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        matcher = PatternMatcher(graph)

        pattern_stars = []
        topic_stars = []
        that_stars = []
        result = matcher.match(PatternMatcherTests.bot, PatternMatcherTests.clientid,
                               Sentence("A B C C2 D"), pattern_stars,
                               Sentence("*"), topic_stars,
                               Sentence("*"), that_stars)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, PatternTemplateNode)
        self.assertEqual(len(pattern_stars), 2)
        self.assertEqual('B', pattern_stars[0])
        self.assertEqual('C C2', pattern_stars[1])
        self.assertEqual(len(topic_stars), 0)
        self.assertEqual(len(that_stars), 0)

        pattern_stars = []
        topic_stars = []
        that_stars = []
        result = matcher.match(PatternMatcherTests.bot, PatternMatcherTests.clientid,
                               Sentence("A B D"), pattern_stars,
                               Sentence("*"), topic_stars,
                               Sentence("*"), that_stars)
        self.assertIsNone(result)
        self.assertEqual(len(pattern_stars), 0)
        self.assertEqual(len(topic_stars), 0)
        self.assertEqual(len(that_stars), 0)

    def test_multiple_stars_with_topic_and_that(self):
        graph = PatternGraph()

        pattern_element = ET.fromstring("<pattern>A * * D</pattern>")
        topic_element = ET.fromstring("<topic>THIS</topic>")
        that_element = ET.fromstring("<that>OTHER</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        matcher = PatternMatcher(graph)

        pattern_stars = []
        topic_stars = []
        that_stars = []
        result = matcher.match(PatternMatcherTests.bot, PatternMatcherTests.clientid,
                               Sentence("A B C C2 D"), pattern_stars,
                               Sentence("THIS"), topic_stars,
                               Sentence("OTHER"), that_stars)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, PatternTemplateNode)
        self.assertEqual(len(pattern_stars), 2)
        self.assertEqual('B', pattern_stars[0])
        self.assertEqual('C C2', pattern_stars[1])
        self.assertEqual(len(topic_stars), 0)
        self.assertEqual(len(that_stars), 0)

    def test_multiple_hashes_with_topic_and_that(self):
        graph = PatternGraph()

        pattern_element = ET.fromstring("<pattern>A # # D</pattern>")
        topic_element = ET.fromstring("<topic>THIS</topic>")
        that_element = ET.fromstring("<that>OTHER</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        matcher = PatternMatcher(graph)

        pattern_stars = []
        topic_stars = []
        that_stars = []
        result = matcher.match(PatternMatcherTests.bot, PatternMatcherTests.clientid,
                               Sentence("A B C C2 D"), pattern_stars,
                               Sentence("THIS"), topic_stars,
                               Sentence("OTHER"), that_stars)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, PatternTemplateNode)
        self.assertEqual(len(pattern_stars), 2)
        self.assertEqual('B', pattern_stars[0])
        self.assertEqual('C C2', pattern_stars[1])
        self.assertEqual(len(topic_stars), 0)
        self.assertEqual(len(that_stars), 0)

    def test_multiple_hashes_with_topic_and_star(self):
        graph = PatternGraph()

        pattern_element = ET.fromstring("<pattern>A # # D</pattern>")
        topic_element = ET.fromstring("<topic>THIS</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        matcher = PatternMatcher(graph)

        pattern_stars = []
        topic_stars = []
        that_stars = []
        result = matcher.match(PatternMatcherTests.bot, PatternMatcherTests.clientid,
                               Sentence("A B C C2 D"), pattern_stars,
                               Sentence("THIS"), topic_stars,
                               Sentence("THAT"), that_stars)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, PatternTemplateNode)
        self.assertEqual(len(pattern_stars), 2)
        self.assertEqual('B', pattern_stars[0])
        self.assertEqual('C C2', pattern_stars[1])
        self.assertEqual(len(topic_stars), 0)
        self.assertEqual(len(that_stars), 1)
        self.assertEqual("THAT", that_stars[0])

    def test_multiple_hashes_with_star_and_that(self):
        graph = PatternGraph()

        pattern_element = ET.fromstring("<pattern>A # # D</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>THAT</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        matcher = PatternMatcher(graph)

        pattern_stars = []
        topic_stars = []
        that_stars = []
        result = matcher.match(PatternMatcherTests.bot, PatternMatcherTests.clientid,
                               Sentence("A B C C2 D"), pattern_stars,
                               Sentence("THIS"), topic_stars,
                               Sentence("THAT"), that_stars)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, PatternTemplateNode)
        self.assertEqual(len(pattern_stars), 2)
        self.assertEqual('B', pattern_stars[0])
        self.assertEqual('C C2', pattern_stars[1])
        self.assertEqual(len(topic_stars), 1)
        self.assertEqual("THIS", topic_stars[0])
        self.assertEqual(len(that_stars), 0)

    def test_simple_priorty(self):
        graph = PatternGraph()

        pattern_element = ET.fromstring("<pattern>$A B C</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        matcher = PatternMatcher(graph)

        pattern_stars = []
        topic_stars = []
        that_stars = []
        result = matcher.match(PatternMatcherTests.bot, PatternMatcherTests.clientid,
                               Sentence("A B C"), pattern_stars,
                               Sentence("*"), topic_stars,
                               Sentence("*"), that_stars)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, PatternTemplateNode)
        self.assertEqual(len(pattern_stars), 0)
        self.assertEqual(len(topic_stars), 0)
        self.assertEqual(len(that_stars), 0)

    def test_mixed_priorty_and_star(self):
        graph = PatternGraph()

        pattern_element1 = ET.fromstring("<pattern>A $B C</pattern>")
        pattern_element2 = ET.fromstring("<pattern>A * C</pattern>")
        pattern_element3 = ET.fromstring("<pattern>A D C</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node1 = TemplateNode()
        template_node2 = TemplateNode()
        template_node3 = TemplateNode()

        graph.add_pattern_to_graph(pattern_element1, topic_element, that_element, template_node1)
        graph.add_pattern_to_graph(pattern_element2, topic_element, that_element, template_node2)
        graph.add_pattern_to_graph(pattern_element3, topic_element, that_element, template_node3)

        matcher = PatternMatcher(graph)

        pattern_stars = []
        topic_stars = []
        that_stars = []
        result = matcher.match(PatternMatcherTests.bot, PatternMatcherTests.clientid,
                               Sentence("A B C"), pattern_stars,
                               Sentence("*"), topic_stars,
                               Sentence("*"), that_stars)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, PatternTemplateNode)
        self.assertEqual(result.template, template_node1)
        self.assertEqual(len(pattern_stars), 0)
        self.assertEqual(len(topic_stars), 0)
        self.assertEqual(len(that_stars), 0)

        pattern_stars = []
        topic_stars = []
        that_stars = []
        result = matcher.match(PatternMatcherTests.bot, PatternMatcherTests.clientid,
                               Sentence("A F C"), pattern_stars,
                               Sentence("*"), topic_stars,
                               Sentence("*"), that_stars)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, PatternTemplateNode)
        self.assertEqual(result.template, template_node2)
        self.assertEqual(len(pattern_stars), 1)
        self.assertEqual("F", pattern_stars[0])
        self.assertEqual(len(topic_stars), 0)
        self.assertEqual(len(that_stars), 0)

        pattern_stars = []
        topic_stars = []
        that_stars = []
        result = matcher.match(PatternMatcherTests.bot, PatternMatcherTests.clientid,
                               Sentence("A D C"), pattern_stars,
                               Sentence("*"), topic_stars,
                               Sentence("*"), that_stars)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, PatternTemplateNode)
        self.assertEqual(result.template, template_node3)
        self.assertEqual(len(pattern_stars), 0)
        self.assertEqual(len(topic_stars), 0)
        self.assertEqual(len(that_stars), 0)

    def test_simple_hash(self):
        graph = PatternGraph()

        pattern_element = ET.fromstring("<pattern>A # C</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        matcher = PatternMatcher(graph)

        pattern_stars = []
        topic_stars = []
        that_stars = []
        result = matcher.match(PatternMatcherTests.bot, PatternMatcherTests.clientid,
                               Sentence("A B C"), pattern_stars,
                               Sentence("*"), topic_stars,
                               Sentence("*"), that_stars)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, PatternTemplateNode)
        self.assertEqual(len(pattern_stars), 1)
        self.assertEqual("B", pattern_stars[0])
        self.assertEqual(len(topic_stars), 0)
        self.assertEqual(len(that_stars), 0)

        pattern_stars = []
        topic_stars = []
        that_stars = []
        result = matcher.match(PatternMatcherTests.bot, PatternMatcherTests.clientid,
                               Sentence("A C"), pattern_stars,
                               Sentence("*"), topic_stars,
                               Sentence("*"), that_stars)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, PatternTemplateNode)
        self.assertEqual(len(pattern_stars), 0)
        self.assertEqual(len(topic_stars), 0)
        self.assertEqual(len(topic_stars), 0)

    def test_simple_hash_at_front(self):
        graph = PatternGraph()

        pattern_element = ET.fromstring("<pattern># B C</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        matcher = PatternMatcher(graph)

        pattern_stars = []
        topic_stars = []
        that_stars = []
        result = matcher.match(PatternMatcherTests.bot, PatternMatcherTests.clientid,
                               Sentence("A B C"), pattern_stars,
                               Sentence("*"), topic_stars,
                               Sentence("*"), that_stars)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, PatternTemplateNode)
        self.assertEqual(len(pattern_stars), 1)
        self.assertEqual('A', pattern_stars[0])
        self.assertEqual(len(topic_stars), 0)
        self.assertEqual(len(that_stars), 0)

        pattern_stars = []
        topic_stars = []
        that_stars = []
        result = matcher.match(PatternMatcherTests.bot, PatternMatcherTests.clientid,
                               Sentence("B C"), pattern_stars,
                               Sentence("*"), topic_stars,
                               Sentence("*"), that_stars)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, PatternTemplateNode)
        self.assertEqual(len(pattern_stars), 0)
        self.assertEqual(len(topic_stars), 0)
        self.assertEqual(len(that_stars), 0)

    def test_simple_hash_at_end(self):
        graph = PatternGraph()

        pattern_element = ET.fromstring("<pattern>A B #</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        matcher = PatternMatcher(graph)

        pattern_stars = []
        topic_stars = []
        that_stars = []
        result = matcher.match(PatternMatcherTests.bot, PatternMatcherTests.clientid,
                               Sentence("A B C"), pattern_stars,
                               Sentence("*"), topic_stars,
                               Sentence("*"), that_stars)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, PatternTemplateNode)
        self.assertEqual(len(pattern_stars), 1)
        self.assertEqual('C', pattern_stars[0])
        self.assertEqual(len(topic_stars), 0)
        self.assertEqual(len(that_stars), 0)

        pattern_stars = []
        topic_stars = []
        that_stars = []
        result = matcher.match(PatternMatcherTests.bot, PatternMatcherTests.clientid,
                               Sentence("A B"), pattern_stars,
                               Sentence("*"), topic_stars,
                               Sentence("*"), that_stars)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, PatternTemplateNode)
        self.assertEqual(len(pattern_stars), 0)
        self.assertEqual(len(topic_stars), 0)
        self.assertEqual(len(that_stars), 0)

    def test_simple_multiple_hashes(self):
        graph = PatternGraph()

        pattern_element = ET.fromstring("<pattern>A # # D</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        matcher = PatternMatcher(graph)

        pattern_stars = []
        topic_stars = []
        that_stars = []
        result = matcher.match(PatternMatcherTests.bot, PatternMatcherTests.clientid,
                               Sentence("A B C D"), pattern_stars,
                               Sentence("*"), topic_stars,
                               Sentence("*"), that_stars)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, PatternTemplateNode)
        self.assertEqual(len(pattern_stars), 2)
        self.assertEqual('B', pattern_stars[0])
        self.assertEqual('C', pattern_stars[1])
        self.assertEqual(len(topic_stars), 0)
        self.assertEqual(len(that_stars), 0)

        pattern_stars = []
        topic_stars = []
        that_stars = []
        result = matcher.match(PatternMatcherTests.bot, PatternMatcherTests.clientid,
                               Sentence("A B D"), pattern_stars,
                               Sentence("*"), topic_stars,
                               Sentence("*"), that_stars)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, PatternTemplateNode)
        self.assertEqual(len(pattern_stars), 1)
        self.assertEqual('B', pattern_stars[0])
        self.assertEqual(len(topic_stars), 0)
        self.assertEqual(len(that_stars), 0)

    def test_simple_topic_and_that(self):
        graph = PatternGraph()

        pattern_element = ET.fromstring("<pattern>A # D</pattern>")
        topic_element = ET.fromstring("<topic>TOPIC1</topic>")
        that_element = ET.fromstring("<that>THAT2</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        matcher = PatternMatcher(graph)

        pattern_stars = []
        topic_stars = []
        that_stars = []
        result = matcher.match(PatternMatcherTests.bot, PatternMatcherTests.clientid,
                               Sentence("A B C D"), pattern_stars,
                               Sentence("TOPIC1"), topic_stars,
                               Sentence("THAT2"), that_stars)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, PatternTemplateNode)
        self.assertEqual(len(pattern_stars), 1)
        self.assertEqual('B C', pattern_stars[0])
        self.assertEqual(len(topic_stars), 0)
        self.assertEqual(len(that_stars), 0)

    def test_simple_star_and_that(self):
        graph = PatternGraph()

        pattern_element = ET.fromstring("<pattern>A * D</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>THAT1</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        matcher = PatternMatcher(graph)

        pattern_stars = []
        topic_stars = []
        that_stars = []
        result = matcher.match(PatternMatcherTests.bot, PatternMatcherTests.clientid,
                               Sentence("A B C D"), pattern_stars,
                               Sentence("TOPIC1"), topic_stars,
                               Sentence("THAT1"), that_stars)
        self.assertIsNotNone(result)
        self.assertEqual(len(pattern_stars), 1)
        self.assertEqual('B C', pattern_stars[0])
        self.assertEqual(len(topic_stars), 1)
        self.assertEqual('TOPIC1', topic_stars[0])
        self.assertEqual(len(that_stars), 0)

    def test_simple_topic_and_star(self):
        graph = PatternGraph()

        pattern_element = ET.fromstring("<pattern>A * D</pattern>")
        topic_element = ET.fromstring("<topic>TOPIC1</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        matcher = PatternMatcher(graph)

        pattern_stars = []
        topic_stars = []
        that_stars = []
        result = matcher.match(PatternMatcherTests.bot, PatternMatcherTests.clientid,
                               Sentence("A B C D"), pattern_stars,
                               Sentence("TOPIC1"), topic_stars,
                               Sentence("THAT1"), that_stars)
        self.assertIsNotNone(result)
        self.assertEqual(len(pattern_stars), 1)
        self.assertEqual('B C', pattern_stars[0])
        self.assertEqual(len(topic_stars), 0)
        self.assertEqual(len(that_stars), 1)
        self.assertEqual('THAT1', that_stars[0])

    def test_simple_multi_branch_star(self):
        graph = PatternGraph()

        pattern_element1 = ET.fromstring("<pattern>A * B C</pattern>")
        pattern_element2 = ET.fromstring("<pattern>A * C D</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        pattern_stars = []
        topic_stars = []
        that_stars = []

        graph.add_pattern_to_graph(pattern_element1, topic_element, that_element, template_node)
        graph.add_pattern_to_graph(pattern_element2, topic_element, that_element, template_node)

        matcher = PatternMatcher(graph)

        result = matcher.match(PatternMatcherTests.bot, PatternMatcherTests.clientid,
                               Sentence("A X Y B C"), pattern_stars,
                               Sentence("*"), topic_stars,
                               Sentence("*"), that_stars)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, PatternTemplateNode)
        self.assertEqual(1, len(pattern_stars))
        self.assertEqual('X Y', pattern_stars[0])
        self.assertEqual(len(topic_stars), 0)
        self.assertEqual(len(that_stars), 0)

    def test_multi_star_multi_branch_star(self):
        graph = PatternGraph()

        pattern_element1 = ET.fromstring("<pattern>A * B * C</pattern>")
        pattern_element2 = ET.fromstring("<pattern>A * C * D</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element1, topic_element, that_element, template_node)
        graph.add_pattern_to_graph(pattern_element2, topic_element, that_element, template_node)

        matcher = PatternMatcher(graph)

        pattern_stars = []
        topic_stars = []
        that_stars = []
        result = matcher.match(PatternMatcherTests.bot, PatternMatcherTests.clientid,
                               Sentence("A X B Y C"), pattern_stars,
                               Sentence("*"), topic_stars,
                               Sentence("*"), that_stars)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, PatternTemplateNode)
        self.assertEqual(2, len(pattern_stars))
        self.assertEqual('X', pattern_stars[0])
        self.assertEqual('Y', pattern_stars[1])
        self.assertEqual(len(topic_stars), 0)
        self.assertEqual(len(that_stars), 0)

    def test_simple_arrow(self):
        graph = PatternGraph()

        pattern_element = ET.fromstring("<pattern>A ^ C</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        matcher = PatternMatcher(graph)

        pattern_stars = []
        topic_stars = []
        that_stars = []
        result = matcher.match(PatternMatcherTests.bot, PatternMatcherTests.clientid,
                               Sentence("A B B B C"), pattern_stars,
                               Sentence("*"), topic_stars,
                               Sentence("*"), that_stars)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, PatternTemplateNode)
        self.assertEqual(1, len(pattern_stars))
        self.assertEqual('B B B', pattern_stars[0])
        self.assertEqual(len(topic_stars), 0)
        self.assertEqual(len(that_stars), 0)

        pattern_stars = []
        topic_stars = []
        that_stars = []
        result = matcher.match(PatternMatcherTests.bot, PatternMatcherTests.clientid,
                               Sentence("A C"), pattern_stars,
                               Sentence("*"), topic_stars,
                               Sentence("*"), that_stars)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, PatternTemplateNode)
        self.assertEqual(len(pattern_stars), 0)
        self.assertEqual(len(topic_stars), 0)
        self.assertEqual(len(that_stars), 0)

    def test_simple_arrow_at_end(self):
        graph = PatternGraph()

        pattern_element = ET.fromstring("<pattern>A B ^</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        matcher = PatternMatcher(graph)

        pattern_stars = []
        topic_stars = []
        that_stars = []
        result = matcher.match(PatternMatcherTests.bot, PatternMatcherTests.clientid,
                               Sentence("A B C"), pattern_stars,
                               Sentence("*"), topic_stars,
                               Sentence("*"), that_stars)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, PatternTemplateNode)
        self.assertEqual(1, len(pattern_stars))
        self.assertEqual('C', pattern_stars[0])
        self.assertEqual(len(topic_stars), 0)
        self.assertEqual(len(that_stars), 0)

        pattern_stars = []
        topic_stars = []
        that_stars = []
        result = matcher.match(PatternMatcherTests.bot, PatternMatcherTests.clientid,
                               Sentence("A B"), pattern_stars,
                               Sentence("*"), topic_stars,
                               Sentence("*"), that_stars)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, PatternTemplateNode)
        self.assertEqual(len(pattern_stars), 0)
        self.assertEqual(len(topic_stars), 0)
        self.assertEqual(len(that_stars), 0)

    def test_simple_arrow_and_hash_at_end(self):
        graph = PatternGraph()

        pattern_element1 = ET.fromstring("<pattern>A ^</pattern>")
        pattern_element2 = ET.fromstring("<pattern>A #</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node1 = TemplateNode()
        template_node2 = TemplateNode()

        graph.add_pattern_to_graph(pattern_element1, topic_element, that_element, template_node1)
        graph.add_pattern_to_graph(pattern_element2, topic_element, that_element, template_node2)

        matcher = PatternMatcher(graph)

        pattern_stars = []
        topic_stars = []
        that_stars = []
        result = matcher.match(PatternMatcherTests.bot, PatternMatcherTests.clientid,
                               Sentence("A C"), pattern_stars,
                               Sentence("*"), topic_stars,
                               Sentence("*"), that_stars)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, PatternTemplateNode)
        self.assertEqual(result.template, template_node2)
        self.assertEqual(1, len(pattern_stars))
        self.assertEqual('C', pattern_stars[0])
        self.assertEqual(len(topic_stars), 0)
        self.assertEqual(len(that_stars), 0)



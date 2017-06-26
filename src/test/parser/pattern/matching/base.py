import logging
import xml.etree.ElementTree as ET

from test.parser.pattern.base import PatternTestBaseClass, TestBot
from programy.dialog import Sentence
from programy.parser.pattern.graph import PatternGraph
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.aiml_parser import AIMLParser

class PatternMatcherBaseClass(PatternTestBaseClass):

    @classmethod
    def setUpClass(cls):
        logging.getLogger().setLevel(logging.DEBUG)
        PatternMatcherBaseClass.bot = TestBot()
        PatternMatcherBaseClass.clientid = "matcher_test"

    def setUp(self):
        self._dump_graph = True
        self.graph = PatternGraph()
        self.matcher =  AIMLParser()

    def dump_graph(self):
        if self._dump_graph is True:
            self.graph.dump()

    def add_pattern_to_graph(self, pattern, topic="*", that="*", template="test"):

        pattern_element = ET.fromstring("<pattern>%s</pattern>"%(pattern))
        topic_element =  ET.fromstring("<topic>%s</topic>"%(topic))
        that_element = ET.fromstring("<that>%s</that>"%(that))
        template_node = TemplateWordNode(template)

        self.matcher.pattern_parser.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

    def match_sentence(self, sentence, topic="*", that="*"):

        return self.matcher.match_sentence( PatternMatcherBaseClass.bot,
                                            PatternMatcherBaseClass.clientid,
                                            Sentence(sentence),
                                            topic,
                                            that)
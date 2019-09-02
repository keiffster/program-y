import xml.etree.ElementTree as ET

from programytest.parser.base import ParserTestsBaseClass, TestBot
from programy.dialog.sentence import Sentence
from programy.parser.template.nodes.word import TemplateWordNode


class PatternMatcherBaseClass(ParserTestsBaseClass):

    def add_pattern_to_graph(self, pattern, topic="*", that="*", template="test"):

        pattern_element = ET.fromstring("<pattern>%s</pattern>"%(pattern))
        topic_element =  ET.fromstring("<topic>%s</topic>"%(topic))
        that_element = ET.fromstring("<that>%s</that>"%(that))
        template_node = TemplateWordNode(template)

        self._client_context.brain.aiml_parser.pattern_parser.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

    def match_sentence(self, sentence, topic="*", that="*"):

        return self._client_context.brain.aiml_parser.match_sentence(self._client_context,
                                                                     Sentence(self._client_context, sentence),
                                                                     topic,
                                                                     that)
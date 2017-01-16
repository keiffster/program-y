"""
Copyright (c) 2016 Keith Sterling

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import logging
from programy.utils.parsing.linenumxml import LineNumberingParser
import xml.etree.ElementTree as ET

from programy.parser.exceptions import ParserException
from programy.config import BrainConfiguration
from programy.parser.pattern.graph import PatternGraph
from programy.parser.pattern.matcher import PatternMatcher
from programy.parser.template.graph import TemplateGraph
from programy.parser.template.evaluator import TemplateEvaluator
from programy.utils.files.filefinder import FileFinder
from programy.dialog import Sentence


class AIMLLoader(FileFinder):
    def __init__(self, aiml_parser):
        FileFinder.__init__(self)
        self.aiml_parser = aiml_parser

    def load_file_contents(self, filename):
        logging.info(filename)
        return self.aiml_parser.parse_from_file(filename)


class AIMLParser(object):
    def __init__(self, supress_warnings=False, stop_on_invalid=False):
        self._supress_warnings = supress_warnings
        self.stop_on_invalid = stop_on_invalid
        self.pattern_parser = PatternGraph()
        self.pattern_matcher = PatternMatcher(self.pattern_parser)
        self.template_parser = TemplateGraph(self)
        self.template_evaluator = TemplateEvaluator()
        self._filename = "Unknown"
        self._version = "Unknown"
        self._aiml_loader = AIMLLoader(self)
        self._num_categories = 0

    @property
    def supress_warnings(self):
        return self._supress_warnings

    @property
    def num_categories(self):
        return self._num_categories

    def load_aiml(self, brain_configuration: BrainConfiguration):
        self._supress_warnings = brain_configuration.supress_warnings
        if brain_configuration.aiml_files is not None:
            aimls_loaded = self._aiml_loader.load_dir_contents(brain_configuration.aiml_files.files,
                                                               brain_configuration.aiml_files.directories,
                                                               brain_configuration.aiml_files.extension)
            logging.info("Loaded a total of %d aiml files", len(aimls_loaded))
        else:
            logging.info("No AIML files defined in configuration to load")

    def parse_from_file(self, filename):
        """
        Parse an AIML file and return all the cateogeries found in the file
        :param filename: Name of file to parse
        :return list of categories parsed from file:
        """
        self._filename = filename

        logging.info("Loading aiml file file: " + self._filename)

        tree = ET.parse(filename, parser=LineNumberingParser())
        aiml = tree.getroot()

        if aiml is None or aiml.tag != 'aiml':
            raise ParserException("Error, root tag is not <aiml>", filename=filename)
        else:
            try:
                self.parse_aiml(aiml, filename)
            except ParserException as parser_excep:
                parser_excep.filename = filename
                raise parser_excep
            except ET.ParseError as xmlpe:
                xmlpe.filename = filename
                xmlpe.xml_exception = xmlpe

    def parse_from_text(self, text):
        """
         Parse an AIML text version of an aiml file and return all the cateogeries found in the file
         :param text: Fully validated AIML snippet
         :return list of categories parsed from file:
         """

        aiml = ET.fromstring(text)

        if aiml is None or aiml.tag != 'aiml':
            ParserException("Error, root tag is not <aiml>", filename="text")
        else:
            self.parse_aiml(aiml, "text")

    #########################################################################################
    #
    #   <?xml version = "1.0" encoding = "UTF-8"?>
    #   <aiml>
    #       <category>
    #           :
    #       </category>
    #       <topic>
    #           <category>
    #           :
    #           </category>
    #       </topic>
    #   </aiml>
    #

    def parse_aiml(self, aiml_xml, filename):
        self.parse_version(aiml_xml)

        categories_found = False
        for expression in aiml_xml:
            if expression.tag == 'topic':
                try:
                    self.parse_topic(expression)
                    categories_found = True
                except ParserException as parser_excep:
                    parser_excep.filename = filename
                    logging.error(parser_excep.format_message())
                    if self.stop_on_invalid is True:
                        raise parser_excep

            elif expression.tag == 'category':
                try:
                    self.parse_category(expression)
                    categories_found = True
                except ParserException as parser_excep:
                    parser_excep.filename = filename
                    logging.error(parser_excep.format_message())
                    if self.stop_on_invalid is True:
                        raise parser_excep

            else:
                raise ParserException("Error, unknown top level tag, %s" % expression.tag, xml_element=expression)

        if categories_found is False:
            logging.warning("no categories in aiml file")
            if self.stop_on_invalid is True:
                raise ParserException("Error, no categories in aiml file", filename=filename)

    #########################################################################################
    #
    # AIML_VERSION ::== 0.9 | 1.0 | 1.1 | 2.0
    #

    def parse_version(self, aiml):
        if 'version' in aiml.attrib:
            self._version = aiml.attrib['version']
            if self._version not in ['0.9', '1.0', '1.1', '2.0']:
                if self._supress_warnings is False:
                    logging.warning("Version number not a supported version: %s", self._version)
        else:
            if self._supress_warnings is False:
                logging.warning("No version info, defaulting to 2.0")
            self._version = "2.0"

    #########################################################################################
    #
    # TOPIC_EXPRESSION:: == <topic name = "PATTERN_EXPRESSION" > (CATEGORY_EXPRESSION) + < / topic >
    #
    # PATTERN_EXPRESSION:: == WORD | PRIORITY_WORD | WILDCARD | SET_STATEMENT | PATTERN_SIDE_BOT_PROPERTY_EXPRESSION
    # PATTERN_EXPRESSION:: == PATTERN_EXPRESSION PATTERN_EXPRESSION
    #
    # This means both topic and that can also be a set of words, stars, hash, sets and bots
    #
    # CATEGORY_EXPRESSION:: == <category>
    #                               <pattern> PATTERN_EXPRESSION </pattern>
    #                              (<that> PATTERN_EXPRESSION </that>)
    #                              (<topic> PATTERN_EXPRESSION </topic>)
    #                              < template > TEMPLATE_EXPRESSION < / template >
    #                          </category>

    def parse_topic(self, topic_element):

        if 'name' in topic_element.attrib:
            name = topic_element.attrib['name']
            if name is None or len(name) == 0:
                raise ParserException("Topic name empty or null", xml_element=topic_element)
            xml = "<topic>%s</topic>" % name
            logging.info("Topic attrib converted to %s", xml)
            topic_pattern = ET.fromstring(xml)
        else:
            raise ParserException("Error, missing name attribute for topic", xml_element=topic_element)

        category_found = False
        for child in topic_element:
            logging.debug(child.tag)
            if child.tag == 'category':
                self.parse_category(child, topic_pattern)
                category_found = True
            else:
                raise ParserException("Error unknown child node of topic, %s" % child.tag, xml_element=topic_element)

        if category_found is False:
            raise ParserException("Error, no categories in topic", xml_element=topic_element)

    def parse_category(self, category_xml, topic_element=None, add_to_graph=True):

        topics = category_xml.findall('topic')
        if topic_element is not None:
            if len(topics) > 0:
                raise ParserException("Error, topic exists in category AND as parent node", xml_element=category_xml)

        else:
            if len(topics) > 1:
                raise ParserException("Error, multiple <topic> nodes found in category", xml_element=category_xml)
            elif len(topics) == 1:
                topic_element = topics[0]
            else:
                topic_element = ET.fromstring("<topic>*</topic>")

        thats = category_xml.findall('that')
        if len(thats) > 1:
            raise ParserException("Error, multiple <that> nodes found in category", xml_element=category_xml)
        elif len(thats) == 1:
            that_element = thats[0]
        else:
            that_element = ET.fromstring("<that>*</that>")

        templates = category_xml.findall('template')
        if len(templates) == 0:
            raise ParserException("Error, no template node found in category", xml_element=category_xml)
        elif len(templates) > 1:
            raise ParserException("Error, multiple <template> nodes found in category", xml_element=category_xml)
        else:
            template_graph_root = self.template_parser.parse_template_expression(templates[0])

        patterns = category_xml.findall('pattern')
        if len(patterns) == 0:
            raise ParserException("Error, no pattern node found in category", xml_element=category_xml)
        elif len(patterns) > 1:
            raise ParserException("Error, multiple <pattern> nodes found in category", xml_element=category_xml)
        else:
            if add_to_graph is True:
                self.pattern_parser.add_pattern_to_graph(patterns[0], topic_element, that_element, template_graph_root)
                self._num_categories += 1

        return (patterns[0], topic_element, that_element, template_graph_root)

    def match_sentence(self, bot, clientid, sentence, parent_question, topic_pattern, that_pattern):
        logging.debug("Matching sentence [%s], topic=[%s], that=[%s] ", sentence.text(), topic_pattern, that_pattern)

        if parent_question is not None:
            pattern_stars = parent_question.current_sentence()._stars
            topic_stars = parent_question.current_sentence()._topicstars
            that_stars = parent_question.current_sentence()._thatstars
        else:
            pattern_stars = sentence._stars
            topic_stars = sentence._topicstars
            that_stars = sentence._thatstars

        matched = self.pattern_matcher.match(bot, clientid,
                                             sentence, pattern_stars,
                                             Sentence(topic_pattern),topic_stars,
                                             Sentence(that_pattern), that_stars)
        if matched is not None:
            return self.template_evaluator.evaluate(bot, clientid, matched.template)

        # pattern_stars = []
        # topic_stars = []
        # that_stars = []
        # matched = self.pattern_matcher.match(bot, clientid, sentence, pattern_stars, Sentence(topic_pattern),
        #                                      topic_stars, Sentence(that_pattern), that_stars)
        # if matched is not None:
        #     if parent_question is not None:
        #         parent_question.current_sentence().stars = pattern_stars
        #         parent_question.current_sentence().topicstars = topic_stars
        #         parent_question.current_sentence().thatstars = that_stars
        #     else:
        #         sentence.stars = pattern_stars
        #         sentence.topicstars = topic_stars
        #         sentence.thatstars = that_stars
        #
        #     return self.template_evaluator.evaluate(bot, clientid, matched.template)

        return None

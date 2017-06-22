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

from programy.utils.parsing.linenumxml import LineNumberingParser
import xml.etree.ElementTree as ET
import logging
import datetime
import os

from programy.parser.exceptions import ParserException, DuplicateGrammarException
from programy.config.brain import BrainConfiguration
from programy.parser.pattern.graph import PatternGraph
from programy.parser.template.graph import TemplateGraph
from programy.utils.files.filefinder import FileFinder
from programy.dialog import Sentence
from programy.parser.pattern.matcher import MatchContext

class AIMLLoader(FileFinder):
    def __init__(self, aiml_parser):
        FileFinder.__init__(self)
        self.aiml_parser = aiml_parser

    def load_file_contents(self, filename):
        try:
            return self.aiml_parser.parse_from_file(filename)
        except Exception as e:
            logging.exception("Failed to load contents of file from [%s]"%filename, e)

class AIMLParser(object):

    def __init__(self, brain=None):
        self._brain = brain
        self.pattern_parser = PatternGraph(aiml_parser=self)
        self.template_parser = TemplateGraph(aiml_parser=self)
        self._aiml_loader = AIMLLoader(self)
        self._num_categories = 0
        self._duplicates = None
        self._errors = None

    @property
    def num_categories(self):
        return self._num_categories

    def create_debug_storage(self, brain_configuration):
        if brain_configuration.aiml_files.errors is not None:
            self._errors = []
        if brain_configuration.aiml_files.duplicates is not None:
            self._duplicates = []

    def save_debug_files(self, brain_configuration):

        if brain_configuration.aiml_files.errors is not None:
            logging.info("Saving aiml errors to file [%s]"%brain_configuration.aiml_files.errors)
            try:
                with open(brain_configuration.aiml_files.errors, "w+") as errors_file:
                    for error in self._errors:
                        errors_file.write(error)
            except Exception as e:
                logging.exception (e)

        if brain_configuration.aiml_files.duplicates is not None:
            logging.info("Saving aiml duplicates to file [%s]"%brain_configuration.aiml_files.duplicates)
            try:
                with open(brain_configuration.aiml_files.duplicates, "w+") as duplicates_file:
                    for duplicate in self._duplicates:
                        duplicates_file.write(duplicate)
            except Exception as e:
                logging.exception (e)

    def display_debug_info(self, brain_configuration):
        if self._errors is not None:
            logging.info("Found a total of %d errors in your grammrs, check out [%s] for details"%(len(self._errors), brain_configuration.aiml_files.errors))
        if self._duplicates is not None:
            logging.info("Found a total of %d duplicate patterns in your grammrs, check out [%s] for details"%(len(self._duplicates), brain_configuration.aiml_files.duplicates))

    def load_files_from_directory(self, brain_configuration):
        start = datetime.datetime.now()
        aimls_loaded = self._aiml_loader.load_dir_contents(brain_configuration.aiml_files.files,
                                                           brain_configuration.aiml_files.directories,
                                                           brain_configuration.aiml_files.extension)
        stop = datetime.datetime.now()
        diff = stop - start
        logging.info("Total processing time %f.2 secs" % diff.total_seconds())
        logging.info("Loaded a total of %d aiml files with %d categories" % (len(aimls_loaded), self.num_categories))
        if diff.total_seconds() > 0:
            logging.info("Thats approx %f aiml files per sec" % (len(aimls_loaded) / diff.total_seconds()))

    def load_single_file(self, brain_configuration):
        start = datetime.datetime.now()
        self._aiml_loader.load_single_file_contents(brain_configuration.aiml_files.file)
        stop = datetime.datetime.now()
        diff = stop - start
        logging.info("Total processing time %f.2 secs" % diff.total_seconds())
        logging.info("Loaded a single aiml file with %d categories" % (self.num_categories))

    def load_aiml(self, brain_configuration: BrainConfiguration):

        if brain_configuration.aiml_files is not None:

            self.create_debug_storage(brain_configuration)

            if brain_configuration.aiml_files.files is not None:
                self.load_files_from_directory(brain_configuration)

            elif brain_configuration.aiml_files.file is not None:
                self.load_single_file(brain_configuration)

            else:
                logging.info("No AIML files or file defined in configuration to load")

            self.save_debug_files(brain_configuration)

            self.display_debug_info(brain_configuration)

        else:
            logging.info("No AIML files or file defined in configuration to load")


        if brain_configuration.dump_to_file is not None:
            logging.debug("Dumping AIML Graph as tree to [%s]"%brain_configuration.dump_to_file)
            self.pattern_parser.dump_to_file(brain_configuration.dump_to_file)

    def parse_from_file(self, filename):
        """
        Parse an AIML file and return all the cateogeries found in the file
        :param filename: Name of file to parse
        :return list of categories parsed from file:
        """
        logging.info("Loading aiml file: " + filename)

        try:
            tree = ET.parse(filename, parser=LineNumberingParser())
            aiml = tree.getroot()
            if aiml is None or aiml.tag != 'aiml':
                raise ParserException("Error, root tag is not <aiml>", filename=filename)
            else:
                self.parse_aiml(aiml, filename)
        except Exception as e:
            logging.exception(e)
            logging.error("Failed to load contents of AIML file from [%s] - [%s]"%(filename, e))


    def parse_from_text(self, text):
        """
         Parse an AIML text version of an aiml file and return all the cateogeries found in the file
         :param text: Fully validated AIML snippet
         :return list of categories parsed from file:
         """

        aiml = ET.fromstring(text)

        if aiml is None or aiml.tag != 'aiml':
            raise ParserException("Error, root tag is not <aiml>")
        else:
            self.parse_aiml(aiml, None)

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

    def handle_aiml_duplicate(self, dupe_excep, filename):
        if self._duplicates is not None:
            dupe_excep.filename = filename
            msg = dupe_excep.format_message()
            self._duplicates.append(msg + "\n")
            logging.error(msg)

    def handle_aiml_error(self, parser_excep, filename):
        parser_excep.filename = filename
        msg = parser_excep.format_message()
        logging.error(msg)

        if self._errors is not None:
            self._errors.append(msg + "\n")

    def parse_aiml(self, aiml_xml, filename):
        self.parse_version(aiml_xml)

        categories_found = False
        for expression in aiml_xml:
            if expression.tag == 'topic':
                try:
                    self.parse_topic(expression)
                    categories_found = True

                except DuplicateGrammarException as dupe_excep:
                    self.handle_aiml_duplicate(dupe_excep, filename)

                except ParserException as parser_excep:
                    self.handle_aiml_error(parser_excep, filename)

            elif expression.tag == 'category':
                try:
                    self.parse_category(expression)
                    categories_found = True

                except DuplicateGrammarException as dupe_excep:
                    self.handle_aiml_duplicate(dupe_excep, filename)

                except ParserException as parser_excep:
                    self.handle_aiml_error(parser_excep, filename)

            else:
                raise ParserException("Error, unknown top level tag, %s" % expression.tag, xml_element=expression)

        if categories_found is False:
            logging.warning("no categories in aiml file")

    #########################################################################################
    #
    # AIML_VERSION ::== 0.9 | 1.0 | 1.1 | 2.0
    #

    def parse_version(self, aiml):
        if 'version' in aiml.attrib:
            version = aiml.attrib['version']
            if version not in ['0.9', '1.0', '1.1', '2.0']:
                logging.warning("Version number not a supported version: %s", version)
        else:
            logging.warning("No version info, defaulting to 2.0")
            version = "2.0"
        return version

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
            if child.tag == 'category':
                self.parse_category(child, topic_pattern)
                category_found = True
            else:
                raise ParserException("Error unknown child node of topic, %s" % child.tag, xml_element=topic_element)

        if category_found is False:
            raise ParserException("Error, no categories in topic", xml_element=topic_element)

    def find_topic(self, category_xml, topic_element=None):
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

        return topic_element

    def find_that(self, category_xml):
        thats = category_xml.findall('that')
        if len(thats) > 1:
            raise ParserException("Error, multiple <that> nodes found in category", xml_element=category_xml)
        elif len(thats) == 1:
            that_element = thats[0]
        else:
            that_element = ET.fromstring("<that>*</that>")
        return that_element

    def get_template(self, category_xml):
        templates = category_xml.findall('template')
        if len(templates) == 0:
            raise ParserException("Error, no template node found in category", xml_element=category_xml)
        elif len(templates) > 1:
            raise ParserException("Error, multiple <template> nodes found in category", xml_element=category_xml)
        else:
            return self.template_parser.parse_template_expression(templates[0])

    def get_pattern(self, category_xml):
        patterns = category_xml.findall('pattern')
        if len(patterns) == 0:
            raise ParserException("Error, no pattern node found in category", xml_element=category_xml)
        elif len(patterns) > 1:
            raise ParserException("Error, multiple <pattern> nodes found in category", xml_element=category_xml)
        else:
            return patterns[0]

    def parse_category(self, category_xml, topic_element=None, add_to_graph=True):

        topic_element = self.find_topic(category_xml, topic_element)

        that_element = self.find_that(category_xml)

        template_graph_root = self.get_template(category_xml)

        pattern = self.get_pattern(category_xml)

        if add_to_graph is True:
            self.pattern_parser.add_pattern_to_graph(pattern, topic_element, that_element, template_graph_root)
            self._num_categories += 1

        return (pattern, topic_element, that_element, template_graph_root)

    def match_sentence(self, bot, clientid, pattern_sentence, topic_pattern, that_pattern):

        topic_sentence = Sentence(topic_pattern)
        that_sentence = Sentence(that_pattern)

        logging.debug("AIML Parser matching sentence [%s], topic=[%s], that=[%s] ", pattern_sentence.text(), topic_pattern, that_pattern)

        sentence = Sentence()
        sentence.append_sentence(pattern_sentence)
        sentence.append_word('__TOPIC__')
        sentence.append_sentence(topic_sentence)
        sentence.append_word('__THAT__')
        sentence.append_sentence(that_sentence)
        logging.debug("Matching [%s]"%sentence.words_from_current_pos(0))

        context = MatchContext()

        template = self.pattern_parser._root_node.match(bot, clientid, context, sentence)

        if template is not None:
            context._template_node = template

            context.list_matches()

            # Save the matched context for the associated sentence
            pattern_sentence.matched_context = context

            return context

        return None

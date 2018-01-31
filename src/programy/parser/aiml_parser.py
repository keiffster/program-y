"""
Copyright (c) 2016-17 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import logging
import datetime
import re
from programy.utils.parsing.linenumxml import LineNumberingParser
import xml.etree.ElementTree as ET

from programy.parser.exceptions import ParserException, DuplicateGrammarException
from programy.config.sections.brain.brain import BrainConfiguration
from programy.parser.pattern.graph import PatternGraph
from programy.parser.template.graph import TemplateGraph
from programy.utils.files.filefinder import FileFinder
from programy.dialog import Sentence
from programy.parser.pattern.matcher import MatchContext
from programy.utils.files.filewriter import ErrorsFileWriter
from programy.utils.files.filewriter import DuplicatesFileWriter
from programy.parser.tokenizer import Tokenizer
from programy.parser.tokenizer import DEFAULT_TOKENIZER


class AIMLLoader(FileFinder):
    def __init__(self, aiml_parser):
        FileFinder.__init__(self)
        self.aiml_parser = aiml_parser

    def load_file_contents(self, filename):
        try:
            return self.aiml_parser.parse_from_file(filename)
        except Exception as excep:
            logging.exception("Failed to load contents of file from [%s]", filename)
            logging.exception(excep)


class AIMLParser(object):
    RE_PATTERN_OF_TAG_AND_NAMESPACE_FROM_TEXT = re.compile("^{.*}.*$")
    RE_MATCH_OF_TAG_AND_NAMESPACE_FROM_TEXT = re.compile("^({.*})(.*)$")

    def __init__(self, brain=None, tokenizer: Tokenizer = DEFAULT_TOKENIZER):
        self._brain = brain
        self._tokenizer = tokenizer
        self.pattern_parser = PatternGraph(aiml_parser=self, tokenizer=tokenizer)
        self.template_parser = TemplateGraph(aiml_parser=self, tokenizer=tokenizer)
        self._aiml_loader = AIMLLoader(self)
        self._num_categories = 0
        self._duplicates = None
        self._errors = None

    def __getstate__(self):
        # We don't need to pickle the File Writes for duplicates and errors,
        # __getstate__ is called during the pickling process to determin whih
        # attributes to load, so we remove the ones we don't want pickling
        d = dict(self.__dict__)
        if '_errors' in d:
            del d['_errors']
        if '_duplicates' in d:
            del d['_duplicates']
        return d

    @property
    def brain(self):
        return self._brain

    @property
    def num_categories(self):
        return self._num_categories

    def create_debug_storage(self, brain_configuration):
        if brain_configuration.files.aiml_files.errors is not None:
            self._errors = ErrorsFileWriter(brain_configuration.files.aiml_files.errors)
        if brain_configuration.files.aiml_files.duplicates is not None:
            self._duplicates = DuplicatesFileWriter(brain_configuration.files.aiml_files.duplicates)

    def save_debug_files(self, brain_configuration):

        if brain_configuration.files.aiml_files.errors is not None:
            num_errors = self._errors.save_content()
            if num_errors > 0:
                print("WARNING:%d errors detected"%num_errors)
                self._errors.print_content()

        if brain_configuration.files.aiml_files.duplicates is not None:
            num_dupes = self._duplicates.save_content()
            if num_dupes > 0:
                print("WARNING: %d duplicated grammars detected"%num_dupes)
                self._duplicates.print_content()

    def display_debug_info(self, brain_configuration):
        if self._errors is not None:
            self._errors.display_debug_info()
        if self._duplicates is not None:
            self._duplicates.display_debug_info()

    def load_files_from_directory(self, brain_configuration):
        start = datetime.datetime.now()
        total_aimls_loaded = 0
        for file in brain_configuration.files.aiml_files.files:
            aimls_loaded = self._aiml_loader.load_dir_contents(file,
                                                               brain_configuration.files.aiml_files.directories,
                                                               brain_configuration.files.aiml_files.extension)
            total_aimls_loaded = len(aimls_loaded)
        stop = datetime.datetime.now()
        diff = stop - start
        if logging.getLogger().isEnabledFor(logging.INFO):
            logging.info("Total processing time %.6f secs", diff.total_seconds())
            logging.info("Loaded a total of %d aiml files with %d categories", total_aimls_loaded, self.num_categories)
        if diff.total_seconds() > 0:
            if logging.getLogger().isEnabledFor(logging.INFO):
                logging.info("Thats approx %f aiml files per sec", total_aimls_loaded / diff.total_seconds())

    def load_single_file(self, brain_configuration):
        start = datetime.datetime.now()
        self._aiml_loader.load_single_file_contents(brain_configuration.files.aiml_files.file)
        stop = datetime.datetime.now()
        diff = stop - start
        if logging.getLogger().isEnabledFor(logging.INFO):
            logging.info("Total processing time %.6f secs", diff.total_seconds())
            logging.info("Loaded a single aiml file with %d categories", self.num_categories)

    def load_aiml(self, brain_configuration: BrainConfiguration):

        if brain_configuration.files.aiml_files is not None:

            self.create_debug_storage(brain_configuration)

            if brain_configuration.files.aiml_files.has_multiple_files():
                self.load_files_from_directory(brain_configuration)

            elif brain_configuration.files.aiml_files.has_single_file():
                self.load_single_file(brain_configuration)

            else:
                if logging.getLogger().isEnabledFor(logging.INFO):
                    logging.info("No AIML files or file defined in configuration to load")

            self.save_debug_files(brain_configuration)

            self.display_debug_info(brain_configuration)

        else:
            if logging.getLogger().isEnabledFor(logging.INFO):
                logging.info("No AIML files or file defined in configuration to load")

    def tag_and_namespace_from_text(self, text):
        # If there is a namespace, then it looks something like
        # {http://alicebot.org/2001/AIML}aiml
        if AIMLParser.RE_PATTERN_OF_TAG_AND_NAMESPACE_FROM_TEXT.match(text) is None:
            # If that pattern does not exist, assume that the text is the tag name
            return text, None

        # Otherwise, extract namespace and tag name
        groupings = AIMLParser.RE_MATCH_OF_TAG_AND_NAMESPACE_FROM_TEXT.match(text)
        if groupings is not None:
            namespace = groupings.group(1).strip()
            tag_name = groupings.group(2).strip()
            return tag_name, namespace
        return None, None

    def tag_from_text(self, text):
        tag, _ = self.tag_and_namespace_from_text(text)
        return tag

    def check_aiml_tag(self, aiml, filename=None):
        # Null check just to be sure
        if aiml is None:
            raise ParserException("Null root tag", filename=filename)

        tag_name, namespace = self.tag_and_namespace_from_text(aiml.tag)

        # Then if check is just <aiml>, thats OK
        if tag_name != 'aiml':
            raise ParserException("Root tag is not <aiml>", filename=filename)

        return tag_name, namespace

    def parse_from_file(self, filename):
        """
        Parse an AIML file and return all the cateogeries found in the file
        :param filename: Name of file to parse
        :return list of categories parsed from file:
        """
        if logging.getLogger().isEnabledFor(logging.INFO):
            logging.info("Loading aiml file: " + filename)

        try:
            tree = ET.parse(filename, parser=LineNumberingParser())
            aiml = tree.getroot()

            _, namespace = self.check_aiml_tag(aiml, filename=filename)

            start = datetime.datetime.now()
            num_categories = self.parse_aiml(aiml, namespace, filename)
            stop = datetime.datetime.now()
            diff = stop - start
            if logging.getLogger().isEnabledFor(logging.INFO):
                logging.info("Processed %s with %d categories in %f.2 secs", filename, num_categories, diff.total_seconds())

        except Exception as excep:
            logging.exception(excep)
            if logging.getLogger().isEnabledFor(logging.ERROR):
                logging.error("Failed to load contents of AIML file from [%s] - [%s]", filename, excep)


    def parse_from_text(self, text):
        """
         Parse an AIML text version of an aiml file and return all the cateogeries found in the file
         :param text: Fully validated AIML snippet
         :return list of categories parsed from file:
         """

        aiml = ET.fromstring(text)

        _, namespace = self.check_aiml_tag(aiml)

        self.parse_aiml(aiml, namespace)

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

    def handle_aiml_duplicate(self, dupe_excep, filename, expression):
        if self._duplicates is not None:
            if logging.getLogger().isEnabledFor(logging.ERROR):
                dupe_excep.filename = filename
                msg = dupe_excep.format_message()
                logging.error(msg)

            startline = None
            if hasattr(expression, "_start_line_number"):
                startline = str(expression._start_line_number)

            endline = None
            if hasattr(expression, "_end_line_number"):
                endline = str(expression._end_line_number)

            self._duplicates.save_entry(dupe_excep.message, filename, startline, endline)

    def handle_aiml_error(self, parser_excep, filename, expression):
        if self._errors is not None:
            if logging.getLogger().isEnabledFor(logging.ERROR):
                parser_excep.filename = filename
                msg = parser_excep.format_message()
                logging.error(msg)

            startline = None
            if hasattr(expression, "_start_line_number"):
                startline = str(expression._start_line_number)

            endline = None
            if hasattr(expression, "_end_line_number"):
                endline = str(expression._end_line_number)

            self._errors.save_entry(parser_excep.message, filename, startline, endline)

    def parse_aiml(self, aiml_xml, namespace, filename=None):
        self.parse_version(aiml_xml)

        categories_found = False
        num_category = 0
        for expression in aiml_xml:
            tag_name, namespace = self.tag_and_namespace_from_text(expression.tag)
            if tag_name == 'topic':
                try:
                    num_topic_categories = self.parse_topic(expression, namespace)
                    num_category += num_topic_categories
                    categories_found = True

                except DuplicateGrammarException as dupe_excep:
                    self.handle_aiml_duplicate(dupe_excep, filename, expression)

                except ParserException as parser_excep:
                    self.handle_aiml_error(parser_excep, filename, expression)

            elif tag_name == 'category':
                try:
                    self.parse_category(expression, namespace)
                    categories_found = True
                    num_category += 1

                except DuplicateGrammarException as dupe_excep:
                    self.handle_aiml_duplicate(dupe_excep, filename, expression)

                except ParserException as parser_excep:
                    self.handle_aiml_error(parser_excep, filename, expression)

            else:
                raise ParserException("Unknown top level tag, %s" % expression.tag, xml_element=expression)

        if categories_found is False:
            if logging.getLogger().isEnabledFor(logging.WARNING):
                logging.warning("no categories in aiml file")

        return num_category

    #########################################################################################
    #
    # AIML_VERSION ::== 0.9 | 1.0 | 1.1 | 2.0
    #

    def parse_version(self, aiml):
        if 'version' in aiml.attrib:
            version = aiml.attrib['version']
            if version not in ['0.9', '1.0', '1.1', '2.0']:
                if logging.getLogger().isEnabledFor(logging.WARNING):
                    logging.warning("Version number not a supported version: %s", version)
        else:
            if logging.getLogger().isEnabledFor(logging.WARNING):
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

    def parse_topic(self, topic_element, namespace):

        if 'name' in topic_element.attrib:
            name = topic_element.attrib['name']
            if name is None or not name:
                raise ParserException("Topic name empty or null", xml_element=topic_element)
            xml = "<topic>%s</topic>" % name
            if logging.getLogger().isEnabledFor(logging.INFO):
                logging.info("Topic attrib converted to %s", xml)
            topic_pattern = ET.fromstring(xml)
        else:
            raise ParserException("Missing name attribute for topic", xml_element=topic_element)

        category_found = False
        num_category = 0
        for child in topic_element:
            tag_name, _ = self.tag_and_namespace_from_text(child.tag)
            if tag_name == 'category':
                self.parse_category(child, namespace, topic_pattern)
                category_found = True
                num_category += 1
            else:
                raise ParserException("Unknown child node of topic, %s" % child.tag, xml_element=topic_element)

        if category_found is False:
            raise ParserException("No categories in topic", xml_element=topic_element)

        return num_category

    def find_all(self, element, name, namespace):
        if namespace is not None:
            search = '%s%s'%(namespace, name)
            return element.findall(search)
        return element.findall(name)

    def find_topic(self, category_xml, namespace, topic_element=None):
        topics = self.find_all(category_xml, "topic", namespace)

        if topic_element is not None:
            if topics:
                raise ParserException("Topic exists in category AND as parent node", xml_element=category_xml)

        else:
            if len(topics) > 1:
                raise ParserException("Multiple <topic> nodes found in category", xml_element=category_xml)
            elif len(topics) == 1:
                topic_element = topics[0]
            else:
                topic_element = ET.fromstring("<topic>*</topic>")

        return topic_element

    def find_that(self, category_xml, namespace):
        thats = self.find_all(category_xml, "that", namespace)
        if len(thats) > 1:
            raise ParserException("Multiple <that> nodes found in category", xml_element=category_xml)
        elif len(thats) == 1:
            that_element = thats[0]
        else:
            that_element = ET.fromstring("<that>*</that>")
        return that_element

    def get_template(self, category_xml, namespace):
        templates = self.find_all(category_xml, "template", namespace)
        if not templates:
            raise ParserException("No template node found in category", xml_element=category_xml)
        elif len(templates) > 1:
            raise ParserException("Multiple <template> nodes found in category", xml_element=category_xml)
        else:
            return self.template_parser.parse_template_expression(templates[0])

    def get_pattern(self, category_xml, namespace):
        patterns = self.find_all(category_xml, "pattern", namespace)
        if not patterns:
            raise ParserException("No pattern node found in category", xml_element=category_xml)
        elif len(patterns) > 1:
            raise ParserException("Multiple <pattern> nodes found in category", xml_element=category_xml)
        else:
            return patterns[0]

    def parse_category(self, category_xml, namespace, topic_element=None, add_to_graph=True):

        topic_element = self.find_topic(category_xml, namespace, topic_element)

        that_element = self.find_that(category_xml, namespace)

        template_graph_root = self.get_template(category_xml, namespace)

        pattern = self.get_pattern(category_xml, namespace)

        if add_to_graph is True:
            self.pattern_parser.add_pattern_to_graph(pattern, topic_element, that_element, template_graph_root)
            self._num_categories += 1

        return (pattern, topic_element, that_element, template_graph_root)

    def match_sentence(self, bot, clientid, pattern_sentence, topic_pattern, that_pattern):

        topic_sentence = Sentence(topic_pattern, tokenizer = self._tokenizer)
        that_sentence = Sentence(that_pattern, tokenizer = self._tokenizer)

        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("AIML Parser matching sentence [%s], topic=[%s], that=[%s] ",
                          pattern_sentence.text(), topic_pattern, that_pattern)

        sentence = Sentence(tokenizer = self._tokenizer)
        sentence.append_sentence(pattern_sentence)
        sentence.append_word('__TOPIC__')
        sentence.append_sentence(topic_sentence)
        sentence.append_word('__THAT__')
        sentence.append_sentence(that_sentence)
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("Matching [%s]", sentence.words_from_current_pos(0))

        context = MatchContext(max_search_depth=bot.configuration.max_search_depth,
                               max_search_timeout=bot.configuration.max_search_timeout)

        template = self.pattern_parser._root_node.match(bot, clientid, context, sentence)

        if template is not None:
            context._template_node = template

            context.list_matches()

            # Save the matched context for the associated sentence
            pattern_sentence.matched_context = context

            return context

        return None

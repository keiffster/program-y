"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

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

from programy.utils.logging.ylogger import YLogger

from programy.utils.text.text import TextUtils
from programy.parser.exceptions import ParserException, DuplicateGrammarException
from programy.parser.pattern.nodes.oneormore import PatternOneOrMoreWildCardNode
from programy.parser.pattern.nodes.zeroormore import PatternZeroOrMoreWildCardNode

#######################################################################################################################
#
class PatternGraph(object):

    def __init__(self, aiml_parser, root_node=None):
        self._aiml_parser = aiml_parser
        self._pattern_factory = aiml_parser.brain.pattern_factory

        self._set_root_node(root_node)

    @property
    def root(self):
        return self._root_node

    @property
    def aiml_parser(self):
        return self._aiml_parser

    @property
    def pattern_factory(self):
        return self._pattern_factory

    def _set_root_node(self, root_node):
        if root_node is None:
            YLogger.debug(self, "Defaulting root to PatternRootNode")
            self._root_node = self._pattern_factory.get_root_node()
        else:
            if root_node.is_root() is False:
                raise ParserException("Root node needs to be of base type PatternRootNode")
            self._root_node = root_node

    def empty(self):
        YLogger.debug(self, "Defaulting root to PatternRootNode")
        self._empty_children(self._root_node)
        self._root_node = self._pattern_factory.get_root_node()

    def _empty_children(self, node):
        for child in node.children:
            self._empty_children(child)
            child.children.clear()

    def node_from_text(self, word, userid="*"):
        if word.startswith("$"):
            node_class = self._pattern_factory.new_node_class('priority')
            return node_class(word[1:], userid)
        elif PatternZeroOrMoreWildCardNode.is_wild_card(word):
            node_class = self._pattern_factory.new_node_class('zeroormore')
            return node_class(word, userid)
        elif PatternOneOrMoreWildCardNode.is_wild_card(word):
            node_class = self._pattern_factory.new_node_class('oneormore')
            return node_class(word, userid)
        node_class = self._pattern_factory.new_node_class('word')
        return node_class(word, userid)

    def node_from_element(self, element, userid="*"):

        node_name = TextUtils.tag_from_text(element.tag)
        if self._pattern_factory.exists(node_name) is False:
            raise ParserException("Unknown node name [%s]"%node_name)

        text = None
        if element.text is not None:
            text = TextUtils.strip_whitespace(element.text)

        node_class_instance = self._pattern_factory.new_node_class(node_name)
        node_instance = node_class_instance(element.attrib, text, userid)

        return node_instance

    def _parse_text(self, pattern_text, current_node, userid="*"):

        stripped = pattern_text.strip()

        words = self._aiml_parser.brain.tokenizer.texts_to_words(stripped)

        for word in words:
            if word != '': # Blank nodes add no value, ignore them
                word = TextUtils.strip_whitespace(word)

                new_node = self.node_from_text(word, userid=userid)

                current_node = current_node.add_child(new_node)

        return current_node

    def get_text_from_element(self, element):
        text = element.text
        if text is not None:
            text = TextUtils.strip_whitespace(text)
            if text == "":
                return None
            return text
        return None

    def get_tail_from_element(self, element):
        text = element.tail
        if text is not None:
            text = TextUtils.strip_whitespace(text)
            if text == "":
                return None
            return text
        return None

    def add_pattern_to_node(self, pattern_element, userid="*"):
        try:

            head_text = self.get_text_from_element(pattern_element)
            if head_text is not None:
                current_node = self._parse_text(head_text, self._root_node, userid=userid)
            else:
                current_node = self._root_node

            for sub_element in pattern_element:
                new_node = self.node_from_element(sub_element)
                current_node = current_node.add_child(new_node)

                tail_text = self.get_tail_from_element(sub_element)
                if tail_text is not None:
                    current_node = self._parse_text(tail_text, current_node)

            return current_node

        except ParserException as parser_excep:
            parser_excep.xml_element = pattern_element
            raise parser_excep

    def add_topic_to_node(self, topic_element, base_node, userid="*"):
        try:

            current_node = self._pattern_factory.new_node_class('topic')(userid)
            current_node = base_node.add_topic(current_node)

            head_text = self.get_text_from_element(topic_element)
            if head_text is not None:
                current_node = self._parse_text(head_text, current_node)

            added_child = False
            for sub_element in topic_element:
                new_node = self.node_from_element(sub_element)
                current_node = current_node.add_child(new_node)

                tail_text = self.get_tail_from_element(sub_element)
                if tail_text is not None:
                    current_node = self._parse_text(tail_text, current_node)
                added_child = True

            if head_text is None:
                if added_child is False:
                    raise ParserException("Topic node text is empty", xml_element=topic_element)

            return current_node

        except ParserException as parser_excep:
            parser_excep.xml_element = topic_element
            raise parser_excep

    def add_that_to_node(self, that_element, base_node, userid="*"):
        try:

            current_node = self._pattern_factory.new_node_class('that')(userid)
            current_node = base_node.add_that(current_node)

            head_text = self.get_text_from_element(that_element)
            if head_text is not None:
                current_node = self._parse_text(TextUtils.strip_whitespace(head_text), current_node)

            added_child = False
            for sub_element in that_element:
                new_node = self.node_from_element(sub_element)
                current_node = current_node.add_child(new_node)

                tail_text = self.get_tail_from_element(sub_element)
                if tail_text is not None:
                    current_node = self._parse_text(tail_text, current_node)
                added_child = True

            if head_text is None:
                if added_child is False:
                    raise ParserException("That node text is empty", xml_element=that_element)

            return current_node

        except ParserException as parser_excep:
            parser_excep.xml_element = that_element
            raise parser_excep

    def add_template_to_node(self, template_graph_root, current_node, userid="*"):
        template_node = self._pattern_factory.new_node_class('template')(template_graph_root, userid)
        current_node = current_node.add_child(template_node, replace_existing=True)
        return current_node

    def add_pattern_to_graph(self, pattern_element, topic_element, that_element, template_graph_root, learn=False, userid="*"):

        pattern_node = self.add_pattern_to_node(pattern_element, userid=userid)

        topic_node = self.add_topic_to_node(topic_element, pattern_node, userid=userid)

        that_node = self.add_that_to_node(that_element, topic_node, userid=userid)

        if that_node.has_template() is True:
            if learn is False:
                if pattern_element.text is not None:
                    raise DuplicateGrammarException("Dupicate grammar tree found [%s]"%(pattern_element.text.strip()))
                else:
                    raise DuplicateGrammarException("Dupicate grammar tree found for bot/set")
            else:
                if pattern_element.text is not None:
                    YLogger.warning(self, "Duplicate grammar tree found [%s] in learn, replacing existing",
                                        pattern_element.text.strip())
                else:
                    YLogger.warning(self, "Duplicate grammar tree found for bot/set in learn, replacing existing")

                self.add_template_to_node(template_graph_root, that_node)
        else:
            self.add_template_to_node(template_graph_root, that_node)

        return that_node

    def count_words_in_patterns(self):
        counter = [0]
        self._count_words_in_children(self._root_node, counter)
        return counter[0]

    def _count_words_in_children(self, node, counter):
        for child in node.children:
            counter[0] += 1
            self._count_words_in_children(child, counter)

    def dump(self, output_func=YLogger.debug, eol="", verbose=True):
        self.root.dump("", output_func, eol, verbose)


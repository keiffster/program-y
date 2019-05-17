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
import xml.etree.ElementTree as ET

######################################################################################################################
#
class TemplateNode(object):

    def __init__(self):
        self._children = []

    @property
    def children(self):
        return self._children

    def append(self, child):
        self._children.append(child)

    def dump(self, tabs, output_func, eol, verbose):
        self.output(tabs, output_func, eol, verbose)

    def output(self, tabs, output_func, eol, verbose):
        self.output_child(self, tabs, eol, output_func)

    def output_child(self, node, tabs, eol, output_func):
        for child in node.children:
            if output_func == print:
                output_func("{0}{1}{2}".format(tabs, child.to_string(), eol))
            else:
                output_func(self, "{0}{1}{2}".format(tabs, child.to_string(), eol))
            self.output_child(child, tabs + "\t", eol, output_func)

    def resolve_children_to_string(self, client_context):
        words = []
        for child in self._children:
            words.append(child.resolve(client_context))

        return client_context.brain.tokenizer.words_to_texts(words)

    def resolve_to_string(self, client_context):
        return self.resolve_children_to_string(client_context)

    def resolve(self, client_context):
        try:
            resolved = self.resolve_to_string(client_context)
            YLogger.debug(client_context, "[%s] resolved to [%s]", self.to_string(), resolved)
            return resolved
        except Exception as excep:
            YLogger.exception(client_context, "Template node failed to resolve", excep)
            return ""

    def to_string(self):
        return "[NODE]"

    def to_xml(self, client_context):
        return self.children_to_xml(client_context)

    def xml_tree(self, client_context):
        xml = "<template>"
        value =  self.children_to_xml(client_context)
        xml += value
        xml += "</template>"
        return ET.fromstring(xml)

    def children_to_xml(self, client_context):
        xml = ""
        first = True
        for child in self.children:
            if first is not True:
                xml += " "
            first = False
            xml += child.to_xml(client_context)
        return xml

    def parse_text(self, graph, text):
        if text is not None:
            string = text.strip()
            if string:
                words = graph.aiml_parser.brain.tokenizer.texts_to_words(string)

                for word in words:
                    if word is not None and word:
                        word_class = graph.get_node_class_by_name('word')
                        word_node = word_class(word.strip())
                        self.children.append(word_node)
                return True
        return False

    def get_text_from_element(self, element):
        text = element.text
        if text is not None:
            text = text.strip()
            return text
        return None

    def get_tail_from_element(self, element):
        text = element.tail
        if text is not None:
            text = text.strip()
            if text == "":
                return None
            return text
        return None

    def parse_template_node(self, graph, pattern):

        head_text = self.get_text_from_element(pattern)
        head_result = self.parse_text(graph, head_text)

        found_sub = False
        for sub_pattern in pattern:
            graph.parse_tag_expression(sub_pattern, self)

            tail_text = self.get_tail_from_element(sub_pattern)
            self.parse_text(graph, tail_text)

            found_sub = True

        if head_result is False and found_sub is False:
            if hasattr(pattern, '_end_line_number'):
                YLogger.warning(self, "No context in template tag at [line(%d), column(%d)]",
                                    pattern._end_line_number,
                                    pattern._end_column_number)
            else:
                YLogger.warning(self, "No context in template tag")

    #######################################################################################################

    def add_default_star(self):
        return False

    def _parse_node(self, graph, expression):
        expression_text = self.parse_text(graph, self.get_text_from_element(expression))

        expression_children = False
        for child in expression:
            graph.parse_tag_expression(child, self)
            self.parse_text(graph, self.get_tail_from_element(child))
            expression_children = True

        if expression_text is False and expression_children is False:
            if self.add_default_star() is True:
                YLogger.debug(self, "Node has no content (text or children), default to <star/>")
                star_class = graph.get_node_class_by_name('star')
                star_node = star_class()
                self.append(star_node)

    #######################################################################################################

    def parse_attrib_value_as_word_node(self, graph, expression, attrib_name):
        node = graph.get_base_node()
        name_node = graph.get_word_node(expression.attrib[attrib_name])
        node.append(name_node)
        return node

    def parse_children_as_word_node(self, graph, child):
        node = graph.get_base_node()
        node.parse_text(graph, self.get_text_from_element(child))
        for sub_child in child:
            graph.parse_tag_expression(sub_child, node)
            node.parse_text(graph, self.get_text_from_element(child))
        return node

    def parse_expression(self, graph, expression):
        raise NotImplementedError("Never call this directly, call the subclass instead!")

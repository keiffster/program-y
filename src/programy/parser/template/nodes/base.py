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
            output_func("%s{%s}%s" % (tabs, child.to_string(), eol))
            self.output_child(child, tabs + "\t", eol, output_func)

    def resolve_children_to_string(self, bot, clientid):
        return (" ".join([child.resolve(bot, clientid) for child in self._children])).strip()

    def resolve(self, bot, clientid):
        try:
            resolved = self.resolve_children_to_string(bot, clientid)
            logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
            return resolved
        except Exception as excep:
            logging.exception(excep)
            return ""

    def to_string(self):
        return "[NODE]"

    def xml_tree(self, bot, clientid):
        param = ["<template>"]
        self.to_xml_children(param, bot, clientid)
        param[0] += "</template>"
        return ET.fromstring(param[0])

    def to_xml(self, bot, clientid):
        xml = ""
        for child in self.children:
            xml += child.to_xml(bot, clientid)
        return xml

    def to_xml_children(self, param, bot, clientid):
        first = True
        for child in self.children:
            if first is False:
                param[0] += " "
            param[0] += child.to_xml(bot, clientid)
            first = False

    def parse_text(self, graph, text):
        if text is not None:
            string = text.strip()
            if len(string) > 0:
                words = string.split(" ")
                for word in words:
                    if word is not None and len(word) > 0:
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
                logging.warning("No context in template tag at [line(%d), column(%d)]" %
                                (pattern._end_line_number,
                                 pattern._end_column_number))
            else:
                logging.warning("No context in template tag")

    #######################################################################################################

    def _parse_node(self, graph, expression):
        expression_text = self.parse_text(graph, self.get_text_from_element(expression))

        expression_children = False
        for child in expression:
            graph.parse_tag_expression(child, self)
            self.parse_text(graph, self.get_tail_from_element(child))
            expression_children = True

        if expression_text is None and expression_children is False:
            logging.debug ("Node has no content (text or children), default to <star/>")
            star_class = graph.get_node_class_by_name('star')
            star_node = star_class()
            self.append(star_node)

    #######################################################################################################

    def _parse_node_with_attrib(self, graph, expression, attrib_name, default_value=None):

        attrib_found = True
        if attrib_name in expression.attrib:
            self.set_attrib(attrib_name, expression.attrib[attrib_name])

        self.parse_text(graph, self.get_text_from_element(expression))

        for child in expression:

            if child.tag == attrib_name:
                self.set_attrib(attrib_name, self.get_text_from_element(child))
            else:
                graph.parse_tag_expression(child, self)

            self.parse_text(graph, self.get_tail_from_element(child))

        if attrib_found is False:
            logging.debug("Setting default value for attrib [%s]", attrib_name)
            self.set_attrib(attrib_name, default_value)

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
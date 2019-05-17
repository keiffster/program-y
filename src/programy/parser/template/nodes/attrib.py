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
from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.word import TemplateWordNode


class TemplateAttribNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)

    def set_attrib(self, attrib_name: str, attrib_value):
        raise NotImplementedError("Should not call this base method, implementation missing")

    #######################################################################################################

    def _parse_node_with_attribs(self, graph, expression, attribs):

        attribs_found = []
        for attrib in attribs:
            attrib_name = attrib[0]
            if attrib_name in expression.attrib:
                self.set_attrib(attrib_name, TemplateWordNode(expression.attrib[attrib_name]))
                attribs_found.append(attrib_name)

        self.parse_text(graph, self.get_text_from_element(expression))

        for child in expression:
            tag_name = TextUtils.tag_from_text(child.tag)

            for attrib in attribs:
                attrib_name = attrib[0]
                if tag_name == attrib_name:
                    self.set_attrib(attrib[0], self.parse_children_as_word_node(graph, child))
                else:
                    graph.parse_tag_expression(child, self)

            self.parse_text(graph, self.get_tail_from_element(child))

        for attrib in attribs:
            attrib_name = attrib[0]
            if attrib_name not in attribs_found:
                if attrib[1] is not None:
                    YLogger.debug(self, "Setting default value for attrib [%s]", attrib_name)
                    self.set_attrib(attrib_name, TemplateWordNode(attrib[1]))

    def _parse_node_with_attrib(self, graph, expression, attrib_name, default_value=None):

        attrib_found = False
        if attrib_name in expression.attrib:
            self.set_attrib(attrib_name, TemplateWordNode(expression.attrib[attrib_name]))
            attrib_found = True

        self.parse_text(graph, self.get_text_from_element(expression))

        for child in expression:
            tag_name = TextUtils.tag_from_text(child.tag)

            if tag_name == attrib_name:
                self.set_attrib(attrib_name, self.parse_children_as_word_node(graph, child))
                attrib_found = True
            else:
                graph.parse_tag_expression(child, self)

            self.parse_text(graph, self.get_tail_from_element(child))

        if attrib_found is False:
            if default_value is not None:
                YLogger.debug(self, "Setting default value for attrib [%s]", attrib_name)
                self.set_attrib(attrib_name, TemplateWordNode(default_value))

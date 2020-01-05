"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

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
from programy.parser.template.nodes.base import TemplateNode
from programy.utils.text.text import TextUtils
from programy.parser.exceptions import ParserException


class TemplateCardNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)
        self._image = None
        self._title = None
        self._subtitle = None
        self._buttons = []

    def resolve_to_string(self, client_context):
        resolved = "<card>"
        resolved += "<title>%s</title>" % self._title.resolve(client_context)

        if self._subtitle is not None:
            resolved += "<subtitle>%s</subtitle>" % self._subtitle.resolve(client_context)

        if self._image is not None:
            resolved += "<image>%s</image>" % self._image.resolve(client_context)

        for button in self._buttons:
            resolved += button.resolve_to_string(client_context)

        resolved += "</card>"
        return resolved

    def to_string(self):
        return "[CARD %d]" % (len(self._buttons))

    def to_xml(self, client_context):
        return self.resolve_to_string(client_context)

    #######################################################################################################
    #

    def parse_expression(self, graph, expression):
        if 'image' in expression.attrib:
            self._image = graph.get_word_node(expression.attrib['image'])

        if 'title' in expression.attrib:
            self._title = graph.get_word_node(expression.attrib['title'])

        if 'subtitle' in expression.attrib:
            self._subtitle = graph.get_word_node(expression.attrib['subtitle'])

        head_text = self.get_text_from_element(expression)
        self.parse_text(graph, head_text)

        for child in expression:
            tag_name = TextUtils.tag_from_text(child.tag)

            if tag_name == 'image':
                self._image = self.parse_children_as_word_node(graph, child)
            elif tag_name == 'title':
                self._title = self.parse_children_as_word_node(graph, child)
            elif tag_name == 'subtitle':
                self._subtitle = self.parse_children_as_word_node(graph, child)
            elif tag_name == 'button':
                button_class = graph.get_node_class_by_name("button")
                button = button_class()
                button.parse_expression(graph, child)
                self._buttons.append(button)
            else:
                raise ParserException("Unsupport child elements of card")

            tail_text = self.get_tail_from_element(child)
            self.parse_text(graph, tail_text)

        if self._title is None:
            raise ParserException("Not title in card")

        if len(self._buttons) == 0:
            raise ParserException("No buttons in card")
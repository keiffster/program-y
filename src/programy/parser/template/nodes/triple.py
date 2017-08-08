"""
Copyright (c) 2016-17 Keith Sterling http://www.keithsterling.com

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

from programy.parser.template.nodes.base import TemplateNode
from programy.utils.text.text import TextUtils
from programy.parser.exceptions import ParserException


class TemplateTripleNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)
        self._subject = None
        self._predicate = None
        self._objective = None

    @property
    def subject(self):
        return self._subject

    @property
    def predicate(self):
        return self._predicate

    @property
    def objective(self):
        return self._objective

    def parse_expression(self, graph, expression):
        if 'subject' in expression.attrib:
            self._subject = expression.attrib['subject']

        if 'predicate' in expression.attrib:
            self._predicate = expression.attrib['predicate']

        if 'objective' in expression.attrib:
            self._objective = expression.attrib['objective']

        head_text = self.get_text_from_element(expression)
        self.parse_text(graph, head_text)

        for child in expression:
            tag_name = TextUtils.tag_from_text(child.tag)

            if tag_name == 'subject':
                self._subject = self.get_text_from_element(child)
            elif tag_name == 'predicate':
                self._predicate = self.get_text_from_element(child)
            elif tag_name == 'objective':
                self._objective = self.get_text_from_element(child)
            else:
                graph.parse_tag_expression(child, self)

            tail_text = self.get_tail_from_element(child)
            self.parse_text(graph, tail_text)

        if self._subject is None:
            raise ParserException("<%s> node missing subject attribue/element"%self._node_name)

        if self._predicate is None:
            raise ParserException("<%s> node missing predicate attribue/element"%self._node_name)

        if self._objective is None:
            raise ParserException("<%s> node missing _objective attribue/element"%self._node_name)




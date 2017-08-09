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
        self._object = None

    @property
    def subject(self):
        return self._subject

    @property
    def predicate(self):
        return self._predicate

    @property
    def object(self):
        return self._object

    def parse_expression(self, graph, expression):
        if 'subj' in expression.attrib:
            self._subject = expression.attrib['subj']

        if 'pred' in expression.attrib:
            self._predicate = expression.attrib['pred']

        if 'obj' in expression.attrib:
            self._object = expression.attrib['obj']

        head_text = self.get_text_from_element(expression)
        self.parse_text(graph, head_text)

        for child in expression:
            tag_name = TextUtils.tag_from_text(child.tag)

            if tag_name == 'subj':
                self._subject = self.get_text_from_element(child)
            elif tag_name == 'pred':
                self._predicate = self.get_text_from_element(child)
            elif tag_name == 'obj':
                self._object = self.get_text_from_element(child)
            else:
                graph.parse_tag_expression(child, self)

            tail_text = self.get_tail_from_element(child)
            self.parse_text(graph, tail_text)

        if self._subject is None:
            raise ParserException("<%s> node missing subject attribue/element"%self._node_name)

        if self._predicate is None:
            raise ParserException("<%s> node missing predicate attribue/element"%self._node_name)

        if self._object is None:
            raise ParserException("<%s> node missing object attribue/element"%self._node_name)




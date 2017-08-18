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
from programy.rdf.entity import RDFEntity


class TemplateTripleNode(TemplateNode):

    def __init__(self, node_name, entity=None):
        TemplateNode.__init__(self)
        self._node_name = node_name
        if entity is None:
            self._entity = RDFEntity()
        else:
            self._entity = entity

    @property
    def node_name(self):
        return self._node_name

    @property
    def entity(self):
        return self._entity

    def children_to_xml(self, bot, clientid):
        return self.entity.to_xml(bot, clientid)

    def parse_expression(self, graph, expression):
        subject = None
        predicate = None
        object = None

        if 'subj' in expression.attrib:
            subject = graph.get_word_node(expression.attrib['subj'])

        if 'pred' in expression.attrib:
            predicate = graph.get_word_node(expression.attrib['pred'])

        if 'obj' in expression.attrib:
            object = graph.get_word_node(expression.attrib['obj'])

        head_text = self.get_text_from_element(expression)
        self.parse_text(graph, head_text)

        for child in expression:
            tag_name = TextUtils.tag_from_text(child.tag)

            if tag_name == 'subj':
                subject = self.parse_children_as_word_node(graph, child)
            elif tag_name == 'pred':
                predicate = self.parse_children_as_word_node(graph, child)
            elif tag_name == 'obj':
                object = self.parse_children_as_word_node(graph, child)
            else:
                graph.parse_tag_expression(child, self)

            tail_text = self.get_tail_from_element(child)
            self.parse_text(graph, tail_text)

        if subject is None:
            raise ParserException("<%s> node missing subject attribue/element"%self.node_name)

        if predicate is None:
            raise ParserException("<%s> node missing predicate attribue/element"%self.node_name)

        if object is None:
            raise ParserException("<%s> node missing object attribue/element"%self.node_name)

        self._entity = RDFEntity(subject=subject, predicate=predicate, object=object)


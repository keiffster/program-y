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


from programy.parser.exceptions import ParserException
from programy.parser.template.nodes.atttrib import TemplateAttribNode
from programy.utils.text.text import TextUtils


class TemplateXMLNode(TemplateAttribNode):

    def __init__(self):
        TemplateAttribNode.__init__(self)
        self._name = None
        self._attribs = {}

    def resolve(self, bot, clientid):
        try:
            xml = "<%s" % self._name
            for attrib_name in self._attribs:
                attrib_value = self._attribs[attrib_name]
                xml += ' %s="%s"' % (attrib_name, attrib_value)
            xml += ">"
            xml += self.resolve_children_to_string(bot, clientid)
            xml += "</%s>" % self._name
            return xml
        except Exception as excep:
            logging.exception(excep)
            return ""

    def to_string(self):
        return "XML"

    def set_attrib(self, attrib_name, attrib_value):
        self._attribs[attrib_name] = attrib_value

    def to_xml(self, bot, clientid):
        xml = "<%s"%self._name
        for attrib_name in self._attribs:
            attrib_value = self._attribs[attrib_name]
            xml += ' %s="%s"'%(attrib_name, attrib_value)
        xml += ">"
        xml += self.children_to_xml(bot, clientid)
        xml += "</%s>"%self._name
        return xml

    def parse_expression(self, graph, expression):
        self._parse_node_with_attribs(graph, expression)

    def _parse_node_with_attribs(self, graph, expression):

        self._name = TextUtils.tag_from_text(expression.tag)

        for attrib_name in expression.attrib:
            self.set_attrib(attrib_name, expression.attrib[attrib_name])

        self.parse_text(graph, self.get_text_from_element(expression))

        for child in expression:
            graph.parse_tag_expression(child, self)
            self.parse_text(graph, self.get_tail_from_element(child))


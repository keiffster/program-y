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
import datetime

from programy.parser.exceptions import ParserException
from programy.parser.template.nodes.atttrib import TemplateAttribNode


class TemplateDateNode(TemplateAttribNode):

    def __init__(self, date_format=None):
        TemplateAttribNode.__init__(self)
        if date_format is None:
            self._format = "%c"
        else:
            self._format = date_format

    @property
    def format(self):
        return self._format

    @format.setter
    def format(self, format):
        self._format = format

    def resolve(self, bot, clientid):
        try:
            time_now = datetime.datetime.now()
            resolved = time_now.strftime(self._format)
            logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
            return resolved
        except Exception as excep:
            logging.exception(excep)
            return ""

    def to_string(self):
        return "DATE format=%s" % (self._format)

    def set_attrib(self, attrib_name, attrib_value):
        if attrib_name != 'format':
            raise ParserException("Invalid attribute name %s for this node" % (attrib_name))
        self._format = attrib_value

    def to_xml(self, bot, clientid):
        xml = '<date format="%s" >' % self._format
        for child in self.children:
            xml += child.to_xml(bot, clientid)
        xml += "</date>"
        return xml

    #######################################################################################################
    # DATE_ATTRIBUTES ::== (format="LISP_DATE_FORMAT") | (jformat="JAVA DATE FORMAT")
    # DATE_ATTRIBUTE_TAG ::== <format>TEMPLATE_EXPRESSION</format> | <jformat>TEMPLATE_EXPRESSION</jformat>
    # DATE_EXPRESSION ::== <date( DATE_ATTRIBUTES)*/> | <date>(DATE_ATTRIBUTE_TAG)</date>
    # Pandorabots supports three extension attributes to the date element in templates:
    #     	locale
    #       format
    #       timezone

    def parse_expression(self, graph, expression):
        self._parse_node_with_attrib(graph, expression, "format", "%c")


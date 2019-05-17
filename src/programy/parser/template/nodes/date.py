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
import datetime
import locale

from programy.parser.exceptions import ParserException
from programy.parser.template.nodes.attrib import TemplateAttribNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.template.nodes.base import TemplateNode


class TemplateDateNode(TemplateAttribNode):

    def __init__(self, date_format=None, locale=None):
        TemplateAttribNode.__init__(self)

        if date_format is None:
            self._format = TemplateWordNode("%c")
        else:
            self._format = TemplateWordNode(date_format)

        self._locale = None
        if locale is not None:
            self._locale = TemplateWordNode(locale)

    def resolve_to_string(self, client_context):
        time_now = datetime.datetime.now()

        local_time = None
        if self._locale is not None:
            local_time = locale.setlocale(locale.LC_TIME)

        try:
            if self._locale is not None:
                locale.setlocale(locale.LC_TIME, self._locale.resolve_to_string(client_context))
            resolved_format = self._format.resolve_to_string(client_context)
            resolved = time_now.strftime(resolved_format)

        finally:
            if local_time is not None:
                locale.setlocale(locale.LC_TIME, local_time)

        YLogger.debug(client_context, "[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        if self._locale is None:
            return "[DATE format=%s]" %self._format.to_string()
        else:
            return "[DATE format=%s locale=%s]"%(self._format.to_string(), self._locale.to_string())

    def set_attrib(self, attrib_name, attrib_value):
        if attrib_name == 'format':
            if isinstance(attrib_value, TemplateNode):
                self._format = attrib_value
            else:
                self._format = TemplateWordNode(attrib_value)

        elif attrib_name == 'locale':
            if isinstance(attrib_value, TemplateNode):
                self._locale = attrib_value
            else:
                self._locale = TemplateWordNode(attrib_value)
        else:
            raise ParserException("Invalid attribute name %s for this node" % (attrib_name))

    def to_xml(self, client_context):
        if self._locale is None:
            xml = '<date format="%s" >' % self._format.to_xml(client_context)
        else:
            xml = '<date format="%s" locale="%s">'%(self._formatto_xml(client_context), self._localeto_xml(client_context))

        xml += self.children_to_xml(client_context)
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
        self._parse_node_with_attribs(graph, expression, [["format", "%c"], ["locale", None]])

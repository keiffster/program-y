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


from programy.parser.exceptions import ParserException
from programy.parser.template.nodes.attrib import TemplateAttribNode
from programy.parser.template.nodes.word import TemplateWordNode



class TemplateLogNode(TemplateAttribNode):

    def __init__(self):
        TemplateAttribNode.__init__(self)
        self._level = TemplateWordNode("debug")
        self._output = TemplateWordNode("logging")

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, level):
        self._level = level

    def resolve_to_string(self, client_context):
        resolved = self.resolve_children_to_string(client_context)

        output = self._output.resolve_to_string(client_context)
        level = self._level.resolve_to_string(client_context)

        if output == "logging":
            YLogger.debug(client_context, "[%s] resolved to [%s]", self.to_string(), resolved)
            if level == "debug":
                YLogger.debug(client_context, resolved)
            elif level == "warning":
                YLogger.warning(client_context, resolved)
            elif level == "error":
                YLogger.error(client_context, resolved)
            elif level == "info":
                YLogger.info(client_context, resolved)
            else:
                YLogger.info(client_context, resolved)
        else:
            print(resolved)

        return ""

    def to_string(self):
        return "[LOG level=%s]" % (self._level.to_string())

    def set_attrib(self, attrib_name, attrib_value):
        if attrib_name != 'level' and attrib_name != 'output':
            raise ParserException("Invalid attribute name %s for this node", attrib_name)

        if attrib_name == 'level':
            if isinstance(attrib_value, TemplateWordNode):
                self._level = attrib_value
            else:
                self._level = TemplateWordNode(attrib_value)
        if attrib_name == 'output':
            if isinstance(attrib_value, TemplateWordNode):
                self._output = attrib_value
            else:
                self._output = TemplateWordNode(attrib_value)

    def to_xml(self, client_context):
        xml = "<log"
        if self._level is not None:
            xml += ' level="%s"' % self._level.to_xml(client_context)
        xml += ">"
        xml += self.children_to_xml(client_context)
        xml += "</log>"
        return xml

    #######################################################################################################
    # LOG_EXPRESSION ::== <log>Message</log>
    #                           <log level="error|warning|debug|info">Message</log>
    #

    def parse_expression(self, graph, expression):
        self._parse_node_with_attribs(graph, expression, [["level", "debug"],["output", "logging"]])

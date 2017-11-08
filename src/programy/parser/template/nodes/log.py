"""
Copyright (c) 2016-17 Keith Sterling http://www.keithsterling.com

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

import logging


from programy.parser.exceptions import ParserException
from programy.parser.template.nodes.attrib import TemplateAttribNode



class TemplateLogNode(TemplateAttribNode):

    def __init__(self):
        TemplateAttribNode.__init__(self)
        self._level = "debug"
        self._output = "logging"

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, level):
        self._level = level

    def resolve_to_string(self, bot, clientid):
        resolved = self.resolve_children_to_string(bot, clientid)

        if self._output == "logging":
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
            if self._level == "debug":
                if logging.getLogger().isEnabledFor(logging.DEBUG):
                    logging.debug(resolved)
            elif self._level == "warning":
                if logging.getLogger().isEnabledFor(logging.WARNING):
                    logging.warning(resolved)
            elif self._level == "error":
                if logging.getLogger().isEnabledFor(logging.ERROR):
                    logging.error(resolved)
            elif self._level == "info":
                if logging.getLogger().isEnabledFor(logging.INFO):
                    logging.info(resolved)
            else:
                if logging.getLogger().isEnabledFor(logging.INFO):
                    logging.info(resolved)
        else:
            print(resolved)
        return ""

    def resolve(self, bot, clientid):
        try:
            return self.resolve_to_string(bot, clientid)
        except Exception as excep:
            logging.exception(excep)
            return ""

    def to_string(self):
        return "LOG level=%s" % (self._level)

    def set_attrib(self, attrib_name, attrib_value):
        if attrib_name != 'level' and attrib_name != 'output':
            raise ParserException("Invalid attribute name %s for this node", attrib_name)
        if attrib_value not in ['debug', 'info', 'warning', 'error'] and \
            attrib_value not in ["logging", "print"]:
            raise ParserException("Invalid attribute value %s for this node %s", attrib_value, attrib_name)
        self._level = attrib_value

    def to_xml(self, bot, clientid):
        xml = "<log"
        if self._level is not None:
            xml += ' level="%s"' % self._level
        xml += ">"
        xml += self.children_to_xml(bot, clientid)
        xml += "</log>"
        return xml

    #######################################################################################################
    # LOG_EXPRESSION ::== <log>Message</log>
    #                           <log level="error|warning|debug|info">Message</log>
    #

    def parse_expression(self, graph, expression):
        self._parse_node_with_attribs(graph, expression, [["level", "debug"],["output", "logging"]])

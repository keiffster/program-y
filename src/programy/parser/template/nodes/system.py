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
import subprocess


from programy.parser.exceptions import ParserException
from programy.parser.template.nodes.atttrib import TemplateAttribNode



class TemplateSystemNode(TemplateAttribNode):

    def __init__(self):
        TemplateAttribNode.__init__(self)
        self._timeout = 0

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, timeout):
        self._timeout = timeout

    def resolve(self, bot, clientid):
        try:
            if bot.brain.configuration.allow_system_aiml is True:
                command = self.resolve_children_to_string(bot, clientid)
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                result = []
                for line in process.stdout.readlines():
                    byte_string = line.decode("utf-8")
                    result.append(byte_string.strip())
                process.wait()
                resolved = " ".join(result)
            else:
                logging.warning("System command node disabled in config")
                resolved = ""
            logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
            return resolved
        except Exception as excep:
            logging.exception(excep)
            return ""

    def to_string(self):
        return "SYSTEM timeout=%s" % (self._timeout)

    def set_attrib(self, attrib_name, attrib_value):
        if attrib_name != 'timeout':
            raise ParserException("Invalid attribute name %s for this node", attrib_name)
        logging.warning("System node timeout attrib currently ignored")
        self._timeout = attrib_value

    def to_xml(self, bot, clientid):
        xml = "<system"
        if self._timeout != 0:
            xml += ' timeout="%d"' % self._timeout
        xml += ">"
        for child in self.children:
            xml += child.to_xml(bot, clientid)
        xml += "</system>"
        return xml

    #######################################################################################################
    # SYSTEM_EXPRESSION ::==
    # 		<system( TIMEOUT_ATTRIBUTE)>TEMPLATE_EXPRESSION</system> |
    #  		<system><timeout>TEMPLATE_EXPRESSION</timeout></system>
    # TIMEOUT_ATTRIBUTE :== timeout=”NUMBER”

    def parse_expression(self, graph, expression):
        self._parse_node_with_attrib(graph, expression, "timeout", "0")


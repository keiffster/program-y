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
import subprocess

from programy.parser.exceptions import ParserException
from programy.parser.template.nodes.attrib import TemplateAttribNode
from programy.parser.template.nodes.word import TemplateWordNode


class TemplateSystemNode(TemplateAttribNode):

    def __init__(self):
        TemplateAttribNode.__init__(self)
        self._timeout = TemplateWordNode("0")

    def resolve_to_string(self, client_context):
        if client_context.brain.configuration.overrides.allow_system_aiml is True:
            command = self.resolve_children_to_string(client_context)
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            result = []
            for line in process.stdout.readlines():
                byte_string = line.decode("utf-8")
                result.append(byte_string.strip())

            process.wait()
            resolved = " ".join(result)

        else:
            YLogger.warning(client_context, "System command node disabled in config")
            resolved = ""

        YLogger.debug(client_context, "[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        return "[SYSTEM timeout=%s]" % (self._timeout.to_string())

    def set_attrib(self, attrib_name, attrib_value):
        if attrib_name != 'timeout':
            raise ParserException("Invalid attribute name %s for this node", attrib_name)
        YLogger.warning(self, "System node timeout attrib currently ignored")
        self._timeout = attrib_value

    def to_xml(self, client_context):
        xml = "<system"

        timeout = self._timeout.to_xml(client_context)

        if timeout != "0":
            xml += ' timeout="%s"' % timeout

        xml += ">"
        xml += self.children_to_xml(client_context)
        xml += "</system>"

        return xml

    #######################################################################################################
    # SYSTEM_EXPRESSION ::==
    # 		<system( TIMEOUT_ATTRIBUTE)>TEMPLATE_EXPRESSION</system> |
    #  		<system><timeout>TEMPLATE_EXPRESSION</timeout></system>
    # TIMEOUT_ATTRIBUTE :== timeout=”NUMBER”

    def parse_expression(self, graph, expression):
        self._parse_node_with_attrib(graph, expression, "timeout", "0")

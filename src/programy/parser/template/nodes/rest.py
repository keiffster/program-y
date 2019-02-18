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

from programy.parser.template.nodes.base import TemplateNode
import json


class TemplateRestNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)

    def resolve_to_string(self, client_context):
        result = self.resolve_children_to_string(client_context)
        resolved = "NIL"
        if result != "":
            try:
                data = json.loads(result)
                if isinstance(data, list):
                    if len(data) > 1:
                        resolved = json.dumps(data[1:])
                else:
                    raise Exception("Not what I wanted")
            except Exception as e:
                words = result.split(" ")
                if words:
                    if len(words) > 1:
                        resolved = " ".join(words[1:])

        YLogger.debug(client_context, "[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        return "[REST]"

    def to_xml(self, client_context):
        xml = "<rest>"
        xml += self.children_to_xml(client_context)
        xml += "</rest>"
        return xml

    #######################################################################################################
    # <implode>ABC</implode>

    def parse_expression(self, graph, expression):
        self._parse_node(graph, expression)

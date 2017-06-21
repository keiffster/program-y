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

from programy.parser.template.nodes.base import TemplateNode


class TemplateIdNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        try:
            logging.debug("[%s] resolved to [%s]", self.to_string(), clientid)
            return clientid
        except Exception as excep:
            logging.exception(excep)
            return ""

    def to_string(self):
        return "ID"

    def to_xml(self, bot, clientid):
        xml = "<id />"
        return xml

    #######################################################################################################
    # <id/> |

    def parse_expression(self, graph, expression):
        self._parse_node(graph, expression)
        if len(self.children) > 0:
            logging.warning("<id> node should not contains child text, use <id /> or <id></id> only")



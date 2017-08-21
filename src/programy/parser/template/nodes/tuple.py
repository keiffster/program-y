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


# Converts the data into a name, value pairs, typically then user by get="?x"
# Expects a string of the format ('?x', 'BIRD'), (None, 'legs'), (None, '2')
class TemplateTupleNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)
        self._pairs = {}

    @property
    def pairs(self):
        return self._pairs

    def get(self, name):
        if name in self._pairs:
            return self._pairs[name]
        else:
            return None

    def resolve(self, bot, clientid):
        try:
            resolved = self.resolve_children_to_string(bot, clientid)
            if logging.getLogger().isEnabledFor(logging.DEBUG): logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
            return resolved
        except Exception as excep:
            logging.exception(excep)
            return ""

    def to_string(self):
        return "TUPLE"

    def to_xml(self, bot, clientid):
        xml = "<tuple>"
        xml += self.children_to_xml(bot, clientid)
        xml += "</tuple>"
        return xml

    #######################################################################################################
    # <tuple>ABC</tuple>

    def parse_expression(self, graph, expression):
        self._parse_node(graph, expression)


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

from random import randint

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.exceptions import ParserException
from programy.utils.text.text import TextUtils


class TemplateRandomNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)

    def resolve_to_string(self, client_context):
        selection = randint(0, (len(self._children) - 1))
        resolved = self._children[selection - 1].resolve(client_context)
        YLogger.debug(client_context, "[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        return "[RANDOM] %d" % (len(self._children))

    def to_xml(self, client_context):
        xml = "<random>"
        for child in self.children:
            xml += "<li>"
            xml += child.to_xml(client_context)
            xml += "</li>"
        xml += "</random>"
        return xml

    #######################################################################################################
    # 	RANDOM_EXPRESSION ::== <random>(<li>TEMPLATE_EXPRESSION</li>)+</random>

    def parse_expression(self, graph, expression):
        li_found = False
        for child in expression:
            tag_name = TextUtils.tag_from_text(child.tag)

            if tag_name == 'li':
                li_found = True
                li_node = graph.get_base_node()
                self.children.append(li_node)
                li_node.parse_template_node(graph, child)
            else:
                raise ParserException("Unsupported random child tag: %s" % (tag_name), xml_element=expression)

        if li_found is False:
            raise ParserException("No li children of random element!", xml_element=expression)

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
from programy.parser.template.nodes.indexed import TemplateIndexedNode



######################################################################################################################
#
# <response index=”n”/> is replaced with the value of the nth previous multi-sentence bot response..
# The response element returns the bot’s response specified by its historical index value.
#
class TemplateResponseNode(TemplateIndexedNode):

    def __init__(self, index=1):
        TemplateIndexedNode.__init__(self, index)

    def resolve_to_string(self, client_context):
        int_index = int(self.index.resolve(client_context))

        conversation = client_context.bot.get_conversation(client_context)
        question = conversation.previous_nth_question(int_index)
        resolved = question.combine_answers()
        YLogger.debug(client_context, "[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        string = "[RESPONSE"
        string += self.index.to_string()
        string += ']'
        return string

    def to_xml(self, client_context):
        xml = '<response index="'
        xml += self.index.to_xml(client_context)
        xml += '"></response>'
        return xml

    #######################################################################################################
    # RESPONSE_EXPRESSION ::== <response( INDEX_ATTRIBUTE)/> | <response><index>TEMPLATE_EXPRESSION</index></response>

    def parse_expression(self, graph, expression):
        self._parse_node_with_attrib(graph, expression, "index", "1")
        if self.children:
            YLogger.warning(self, "<response> node should not contain child text, use <response /> or <response></response> only")

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
from programy.parser.template.nodes.indexed import TemplateIndexedNode



######################################################################################################################
#
# <response index=”n”/> is replaced with the value of the nth previous multi-sentence bot response..
# The response element returns the bot’s response specified by its historical index value.
#
class TemplateResponseNode(TemplateIndexedNode):

    def __init__(self, index=1):
        TemplateIndexedNode.__init__(self, index)

    def resolve_to_string(self, bot, clientid):
        conversation = bot.get_conversation(clientid)
        question = conversation.previous_nth_question(self.index)
        resolved = question.combine_answers()
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def resolve(self, bot, clientid):
        try:
            return self.resolve_to_string(bot, clientid)
        except Exception as excep:
            logging.exception(excep)
            return ""

    def to_string(self):
        string = "RESPONSE"
        string += self.get_index_as_str()
        return string

    def to_xml(self, bot, clientid):
        xml = "<response"
        xml += self.get_index_as_xml()
        xml += ">"
        xml += "</response>"
        return xml

    #######################################################################################################
    # RESPONSE_EXPRESSION ::== <response( INDEX_ATTRIBUTE)/> | <response><index>TEMPLATE_EXPRESSION</index></response>

    def parse_expression(self, graph, expression):
        self._parse_node_with_attrib(graph, expression, "index", "1")
        if self.children:
            if logging.getLogger().isEnabledFor(logging.WARNING):
                logging.warning("<response> node should not contains child text, use <response /> or <response></response> only")

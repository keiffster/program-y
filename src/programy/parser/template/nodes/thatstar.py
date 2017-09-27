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

from programy.parser.template.nodes.indexed import TemplateDoubleIndexedNode


#####################################################################################################################
#
class TemplateThatStarNode(TemplateDoubleIndexedNode):

    def __init__(self, question=1, sentence=1):
        TemplateDoubleIndexedNode.__init__(self, question, sentence)

    def resolve_to_string(self, bot, clientid):
        conversation = bot.get_conversation(clientid)

        question = conversation.previous_nth_question(self.question - 1)

        sentence = question.current_sentence()

        resolved = sentence.matched_context.thatstar(self.sentence)

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
        string = "THATSTAR"
        string += self.get_question_and_sentence_as_str()
        return string

    def to_xml(self, bot, clientid):
        xml = "<thatstar"
        xml += self.get_question_and_sentence_as_index_xml()
        xml += "></thatstar>"
        return xml

    #######################################################################################################
    # THATSTAR_EXPRESSION ::== <thatstar( INDEX_ATTRIBUTE)/> | <thatstar><index>TEMPLATE_EXPRESSION</index></thatstar>

    def parse_expression(self, graph, expression):
        self._parse_node_with_attrib(graph, expression, "index", "1,1")

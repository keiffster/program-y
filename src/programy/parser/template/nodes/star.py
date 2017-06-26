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

from programy.parser.template.nodes.indexed import TemplateIndexedNode

#TODO If the index exceeds the number of stars then an exception is thrown, it should write an error and return None
class TemplateStarNode(TemplateIndexedNode):

    def __init__(self, position=1, index=1):
        TemplateIndexedNode.__init__(self, position, index)

    def resolve(self, bot, clientid):
        try:
            conversation = bot.get_conversation(clientid)
            current_question = conversation.current_question()
            current_sentence = current_question.current_sentence()
            matched_context = current_sentence.matched_context

            if matched_context is None:
                logging.error("Star node has no matched context for clientid %s" % (clientid))
                resolved = ""

            resolved = matched_context.star(self.index)

            if resolved is None:
                logging.error("Star index not in range [%d]"%(self.index))
                resolved = ""

            logging.debug("Star Node [%s] resolved to [%s]", self.to_string(), resolved)
            return resolved

        except Exception as excep:
            logging.exception(excep)
            return ""

    def to_string(self):
        return "STAR Index=%s" % self.index

    def to_xml(self, bot, clientid):
        xml = "<star"
        if self._position > 1:
            xml += ' position="%d"' % self._position
        if self._index > 1:
            xml += ' index="%d"' % self._index
        xml += ">"
        xml += "</star>"
        return xml

    #######################################################################################################
    # INDEX_ATTRIBUTE ::== index="NUMBER"
    # STAR_EXPRESSION ::== <star( INDEX_ATTRIBUTE)/> | <star><index>TEMPLATE_EXPRESSION</index></star>

    def parse_expression(self, graph, expression):
        self._parse_node_with_attrib(graph, expression, "index", "1")


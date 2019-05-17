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
# <topicstar />
# <topicstar index=”n” />
# The topicstar element will either return the current topic if used outside of a topic element or the wildcard
# element when inside a topic element. The topicstar element can also use index like the star element can, though
# this will return as the default case for empty predicates if no wildcards are present.

class TemplateTopicStarNode(TemplateIndexedNode):

    def __init__(self, index=1):
        TemplateIndexedNode.__init__(self, index)

    def resolve_to_string(self, client_context):
        int_index = int(self.index.resolve(client_context))

        conversation = client_context.bot.get_conversation(client_context)
        question = conversation.current_question()
        sentence = question.current_sentence()
        resolved = sentence.matched_context.topicstar(int_index)
        YLogger.debug(client_context, "[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        string = "[TOPICSTAR"
        string += self.index.to_string() + ']'
        return string

    def to_xml(self, client_context):
        xml = '<topicstar index="'
        xml += self.index.to_xml(client_context)
        xml += '">'
        xml += "</topicstar>"
        return xml

    #######################################################################################################
    # TOPICSTAR_EXPRESSION ::== <topicstar( INDEX_ATTRIBUTE)/> | <topicstar><index>TEMPLATE_EXPRESSION</index></topicstar>

    def parse_expression(self, graph, expression):
        self._parse_node_with_attrib(graph, expression, "index", "1")

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


class TemplateStarNode(TemplateIndexedNode):

    def __init__(self, index=1):
        TemplateIndexedNode.__init__(self, index)

    def resolve_to_string(self, client_context):
        conversation = client_context.bot.get_conversation(client_context)

        if conversation.has_current_question():

            current_question = conversation.current_question()

            current_sentence = current_question.current_sentence()

            matched_context = current_sentence.matched_context
            if matched_context is None:
                YLogger.error(client_context, "Star node has no matched context for clientid %s", client_context.userid)
                resolved = ""
            else:
                int_index = int(self.index.resolve(client_context))
                try:
                    resolved = matched_context.star(int_index)
                    if resolved is None:
                        YLogger.error(client_context, "Star index not in range [%d]", int_index)
                        resolved = ""
                except Exception:
                    YLogger.error(client_context, "Star index not in range [%d]", self.index)
                    resolved = ""
        else:
            resolved = ""

        YLogger.debug(client_context, "Star Node [%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        string = "[STAR"
        string += self.index.to_string() + ']'
        return string

    def to_xml(self, client_context):
        xml = '<star index="'
        xml += self.index.to_xml(client_context)
        xml += '"></star>'
        return xml

    #######################################################################################################
    # INDEX_ATTRIBUTE ::== index="NUMBER"
    # STAR_EXPRESSION ::== <star( INDEX_ATTRIBUTE)/> | <star><index>TEMPLATE_EXPRESSION</index></star>

    def parse_expression(self, graph, expression):
        self._parse_node_with_attrib(graph, expression, "index", "1")

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

class TemplateEvalNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        try:
            resolved = self.resolve_children_to_string(bot, clientid)
            logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
            return resolved
        except Exception as excep:
            logging.exception(excep)
            return ""

    def to_string(self):
        return "EVAL"

    def to_xml(self, bot, clientid):
        xml = "<eval>"
        for child in self.children:
            xml += child.to_xml(bot, clientid)
        xml += "</eval>"
        return xml

    #######################################################################################################
    # EVAL_EXPRESSION ::== <eval>TEMPLATE_EXPRESSION</eval>
    #
    # LEARN_PATTERN_EXPRESSION ::== PATTERN_EXPRESSION | EVAL_EXPRESSION
    # LEARN_PATTERN_EXPRESSION ::== (LEARN_PATTERN_EXPRESSION)+
    #
    # LEARN_TEMPLATE_EXPRESSION ::== TEXT | TAG_EXPRESSION | EVAL_EXPRESSION
    #
    # LEARN_TEMPLATE_EXPRESSION ::== (LEARN_TEMPLATE_EXPRESSION)*
    #
    # LEARN_CATEGORY_EXPRESSION ::==
    # 						<category>
    # 							<pattern>LEARN_PATTERN_EXPRESSION</pattern>
    # 							(<that>LEARN_PATTERN_EXPRESSION</that>)
    # 							(<topic>LEARN_PATTERN_EXPRESSION</topic>)
    # 							<template>LEARN_TEMPLATE_EXPRESSION</template>
    # 						</category>
    #
    # LEARN_EXPRESSION ::== 	<learn>LEARN_CATEGORY_EXPRESSION</learn> |
    # 						<learnf>LEARN_CATEGORY_EXPRESSION</learnf>

    def parse_expression(self, graph, expression):

        head_text = self.get_text_from_element(expression)
        self.parse_text(graph, head_text)

        for child in expression:
            graph.parse_tag_expression(child, self)

            tail_text = self.get_tail_from_element(child)
            self.parse_text(graph, tail_text)


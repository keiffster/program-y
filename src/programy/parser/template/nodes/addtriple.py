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

from programy.parser.template.nodes.triple import TemplateTripleNode

class TemplateAddTripleNode(TemplateTripleNode):

    def __init__(self, entity=None):
        TemplateTripleNode.__init__(self, node_name="addtriple", entity=entity)

    def resolve(self, bot, clientid):
        try:
            subject = self.entity.subject.resolve(bot, clientid)
            predicate = self.entity.predicate.resolve(bot, clientid)
            object = self.entity.object.resolve(bot, clientid)

            bot.brain.rdf.add_entity(subject, predicate, object)
            resolved = ""
            if logging.getLogger().isEnabledFor(logging.DEBUG): logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
            return resolved
        except Exception as excep:
            logging.exception(excep)
            return ""

    def to_string(self):
        return "ADDTRIPLE"

    def to_xml(self, bot, clientid):
        xml = "<addtriple>"
        xml += self.children_to_xml(bot, clientid)
        xml += "</addtriple>"
        return xml

    #######################################################################################################
    # ADDTRIPLE_EXPRESSION ::== <addtriple>TEMPLATE_EXPRESSION</addtriple>

    def parse_expression(self, graph, expression):
        super(TemplateAddTripleNode, self).parse_expression(graph, expression)


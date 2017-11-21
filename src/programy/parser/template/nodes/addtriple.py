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

from programy.parser.template.nodes.triple import TemplateTripleNode
from programy.parser.exceptions import ParserException


class TemplateAddTripleNode(TemplateTripleNode):

    def __init__(self, subj=None, pred=None, obj=None):
        TemplateTripleNode.__init__(self, node_name="addtriple", subj=subj, pred=pred, obj=obj)

    def resolve_to_string(self, bot, clientid):
        rdf_subject = self._subj.resolve(bot, clientid)
        rdf_predicate = self._pred.resolve(bot, clientid)
        rdf_object = self._obj.resolve(bot, clientid)

        bot.brain.rdf.add_entity(rdf_subject, rdf_predicate, rdf_object)
        resolved = ""
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

        if self._subj is None:
            raise ParserException("<%s> node missing subject attribue/element"%self.node_name)

        if  self._pred is None:
            raise ParserException("<%s> node missing predicate attribue/element"%self.node_name)

        if self._obj is None:
            raise ParserException("<%s> node missing object attribue/element"%self.node_name)

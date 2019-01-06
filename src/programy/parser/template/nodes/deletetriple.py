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

from programy.parser.template.nodes.triple import TemplateTripleNode
from programy.parser.exceptions import ParserException


class TemplateDeleteTripleNode(TemplateTripleNode):

    def __init__(self, subj=None, pred=None, obj=None):
        TemplateTripleNode.__init__(self, node_name="deletetriple", subj=subj, pred=pred, obj=obj)

    def resolve_to_string(self, client_context):
        rdf_subject = self._subj.resolve(client_context)
        rdf_predicate = self._pred.resolve(client_context)
        rdf_object = self._obj.resolve(client_context)

        resolved = ""
        client_context.brain.rdf.delete_entity(rdf_subject, rdf_predicate, rdf_object)
        YLogger.debug(client_context, "[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        return "[DELETETRIPLE]"

    def to_xml(self, client_context):
        xml = "<deletetriple>"
        xml += self.children_to_xml(client_context)
        xml += "</deletetriple>"
        return xml

    #######################################################################################################
    # DELETETRIPLE_EXPRESSION ::== <deletetriple>TEMPLATE_EXPRESSION</deletetriple>

    def parse_expression(self, graph, expression):
        super(TemplateDeleteTripleNode, self).parse_expression(graph, expression)

        if self._subj is None:
            raise ParserException("<%s> node missing subject attribue/element"%self.node_name)

        if  self._pred is None:
            YLogger.debug(self, "<%s> node missing predicate attribue/element", self.node_name)

        if self._obj is None:
            YLogger.debug(self, "<%s> node missing object attribue/element", self.node_name)

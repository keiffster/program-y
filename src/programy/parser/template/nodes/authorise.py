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

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.exceptions import ParserException

class TemplateAuthoriseNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)
        self._role = None
        self._denied_srai = None

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, role):
        self._role = role

    @property
    def denied_srai(self):
        return self._denied_srai

    @denied_srai.setter
    def denied_srai(self, denied_srai):
        self._denied_srai = denied_srai

    def resolve_to_string(self, client_context):
        # Check if the user, role or group exists, assumption being, that if defined
        # in the tag and exists then we can execute the inner children
        # Assumption is that user has been authenticated and passed and is value
        if client_context.brain.security.authorisation is not None:
            if client_context.brain.security.authorisation.authorise(client_context.userid, self.role) is False:
                if self._denied_srai is not None:
                    srai_text = self._denied_srai
                else:
                    srai_text = client_context.brain.security.authorisation.get_default_denied_srai()
                resolved = client_context.bot.ask_question(client_context, srai_text, srai=True)
                YLogger.debug(self, "[%s] resolved to [%s]", self.to_string(), resolved)
                return resolved

        # Resolve afterwards, as pointless resolving before checking for authorisation
        resolved = self.resolve_children_to_string(client_context)
        YLogger.debug(self, "[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        text = "[AUTHORISE ("
        text += "role=%s"%self._role
        if self._denied_srai is not None:
            text += ", denied_srai=%s"%self._denied_srai
        text += ")]"
        return text

    def to_xml(self, client_context):
        xml = '<authorise'
        xml += ' role="%s"' % self._role
        if self._denied_srai is not None:
            xml += ' denied_srai="%s"' % self._denied_srai
        xml += '>'
        xml += self.children_to_xml(client_context)
        xml += '</authorise>'
        return xml

    #######################################################################################################
    # AUTHORISE_ATTRIBUTES ::= role="ROLEID" [, denied_srai="SRAI_TAG"]
    # AUTHORISE_EXPRESSION ::== <authorise( AUTHORISE_ATTRIBUTES)*>TEMPLATE_EXPRESSION</authorise> |

    def parse_expression(self, graph, expression):

        if 'role' in expression.attrib:
            self._role = expression.attrib['role']

        if self._role is None:
            raise ParserException("AUTHORISE role attribute missing !")

        if 'denied_srai' in expression.attrib:
            self._denied_srai = expression.attrib['denied_srai']

        head_text = self.get_text_from_element(expression)
        self.parse_text(graph, head_text)

        for child in expression:
            graph.parse_tag_expression(child, self)
            tail_text = self.get_tail_from_element(child)
            self.parse_text(graph, tail_text)

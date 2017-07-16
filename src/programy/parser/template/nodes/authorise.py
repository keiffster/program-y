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

from programy.parser.template.nodes.base import TemplateNode
from programy.utils.services.service import ServiceFactory
from programy.parser.exceptions import ParserException

class TemplateAuthoriseNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)
        self._user = None
        self._role = None
        self._group = None

    @property
    def user(self):
        return self._user

    @property
    def role(self):
        return self._role

    @property
    def group(self):
        return self._group

    def resolve(self, bot, clientid):
        try:
            # Check if the user, role or group exists, assumption being, that if defined
            # in the tag and exists then we can execute the inner children
            # Assumpetion is that user has been authenticated and passed and is value
            if self._user is not None:
                bot.brain.authorisation.authorise_for_user(clientid, self._user)
            if self._role is not None:
                bot.brain.authorisation.authorise_for_role(clientid, self._role)
            if self._role is not None:
                bot.brain.authorisation.authorise_for_group(clientid, self._group)
            else:
                raise Exception("Unknown authorisation defined!")

            # Resolve afterwards, as pointless resolving before checking for authorisation
            resolved = self.resolve_children_to_string(bot, clientid)
            logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
            return resolved

        except Exception as excep:
            logging.exception(excep)
            return ""

    def to_string(self):
        text = "AUTHORISE ("
        if self._user is not None:
            text += "user=%s"%self._user
        if self._role is not None:
            text += "role=%s"%self._role
        if self._group is not None:
            text += "group=%s"%self._group
        text += ")"

    def to_xml(self, bot, clientid):
        xml = '<authorise'
        if self._service is not None:
            if self._user is not None:
                xml += 'user="%s"' % self._user
            if self._role is not None:
                xml += 'role="%s"' % self._role
            if self._group is not None:
                xml += 'group="%s"' % self._group
        xml += '>'
        xml += self.children_to_xml(bot, clientid)
        xml += '</authorise>'
        return xml

    #######################################################################################################
    # AUTHORISE_ATTRIBUTES ::= role="ROLEID" | group="GROUPID" | user="USERID"
    # AUTHORISE_EXPRESSION ::== <authorise( AUTHORISE_ATTRIBUTES)*>TEMPLATE_EXPRESSION</authorise> |

    def parse_expression(self, graph, expression):

        if 'user' in expression.attrib:
            self._user = expression.attrib['user']
        if 'role' in expression.attrib:
            self._role = expression.attrib['role']
        if 'group' in expression.attrib:
            self._group = expression.attrib['group']

        if self._user is None and self._role is None and self._group is None:
            raise ParserException("AUTHORISE node, user, role or group attribute missing !")

        head_text = self.get_text_from_element(expression)
        self.parse_text(graph, head_text)

        for child in expression:
            graph.parse_tag_expression(child, self)
            tail_text = self.get_tail_from_element(child)
            self.parse_text(graph, tail_text)


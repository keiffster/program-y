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
from programy.services.service import ServiceFactory
from programy.parser.exceptions import ParserException
from programy.utils.text.text import TextUtils

class TemplateSRAIXNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)
        self._service = None

    @property
    def service(self):
        return self._service

    @service.setter
    def service(self, service):
        self._service = service

    def resolve_to_string(self, client_context):
        resolved = self.resolve_children_to_string(client_context)
        YLogger.debug(client_context, "[%s] resolved to [%s]", self.to_string(), resolved)

        if self._service is not None:
            bot_service = ServiceFactory.get_service(self._service)
            response = bot_service.ask_question(client_context, resolved)
            YLogger.debug(client_context, "SRAIX service [%s] return [%s]", self._service, response)
            return response
        else:
            YLogger.error(client_context, "Sorry SRAIX does not currently have an implementation for [%s]", self._service)
            return ""

    def to_string(self):
        if self._service is not None:
            return "[SRAIX (service=%s)]" % (self._service)
        return "[SRAIX ()]"

    def to_xml(self, client_context):
        xml = '<sraix'
        if self._service is not None:
            xml += ' service="%s"' % self.service
        xml += '>'
        xml += self.children_to_xml(client_context)
        xml += '</sraix>'
        return xml

    #######################################################################################################
    # SRAIX_ATTRIBUTES ::= host="HOSTNAME" | botid="BOTID" | hint="TEXT" | apikey="APIKEY" | service="SERVICE"
    # SRAIX_ATTRIBUTE_TAGS ::= <host>TEMPLATE_EXPRESSION</host> | <botid>TEMPLATE_EXPRESSION</botid> |
    # <hint>TEMPLATE_EXPRESSION</hint> | <apikey>TEMPLATE_EXPRESSION</apikey> | <service>TEMPLATE_EXPRESSION</service>
    # SRAIX_EXPRESSION ::== <sraix( SRAIX_ATTRIBUTES)*>TEMPLATE_EXPRESSION</sraix> |

    def parse_expression(self, graph, expression):

        if 'host' in expression.attrib:
            YLogger.warning(self, "'host' attrib not supported in sraix, moved to config, see documentation")
        if 'botid' in expression.attrib:
            YLogger.warning(self, "'botid' attrib not supported in sraix, moved to config, see documentation")
        if 'hint' in expression.attrib:
            YLogger.warning(self, "'hint' attrib not supported in sraix, moved to config, see documentation")
        if 'apikey' in expression.attrib:
            YLogger.warning(self, "'apikey' attrib not supported in sraix, moved to config, see documentation")

        if 'service' in expression.attrib:
            self.service = expression.attrib['service']

        head_text = self.get_text_from_element(expression)
        self.parse_text(graph, head_text)

        for child in expression:
            tag_name = TextUtils.tag_from_text(child.tag)

            if tag_name == 'host':
                YLogger.warning(self, "'host' element not supported in sraix, moved to config, see documentation")
            elif tag_name == 'botid':
                YLogger.warning(self, "'botid' element not supported in sraix, moved to config, see documentation")
            elif tag_name == 'hint':
                YLogger.warning(self, "'hint' element not supported in sraix, moved to config, see documentation")
            elif tag_name == 'apikey':
                YLogger.warning(self, "'apikey' element not supported in sraix, moved to config, see documentation")
            elif tag_name == 'service':
                self.service = self.get_text_from_element(child)
            else:
                graph.parse_tag_expression(child, self)

            tail_text = self.get_tail_from_element(child)
            self.parse_text(graph, tail_text)

        if self.service is None:
            raise ParserException("SRAIX node, service attribute missing !")

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
from programy.utils.services.service import ServiceFactory


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

    def resolve(self, bot, clientid):
        try:
            resolved = self.resolve_children_to_string(bot, clientid)
            logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)

            if self._service is not None:
                bot_service = ServiceFactory.get_service(self._service)
                response = bot_service.ask_question(bot, clientid, resolved)
                logging.debug("SRAIX service [%s] return [%s]", self._service, response)
                return response
            else:
                logging.error("Sorry SRAIX does not currently have an implementation for [%s]", self._service)
                return ""

        except Exception as excep:
            logging.exception(excep)
            return ""

    def to_string(self):
        return "SRAIX (service=%s)" % (self._service)

    def to_xml(self, bot, clientid):
        xml = '<sraix'
        if self._service is not None:
            xml += ' service="%s"' % self.service
        xml += '>'
        for child in self.children:
            xml += child.to_xml(bot, clientid)
        xml += '</sraix>'
        return xml

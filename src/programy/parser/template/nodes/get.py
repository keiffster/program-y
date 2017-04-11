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



class TemplateGetNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)
        self._name = None
        self._local = False

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def local(self):
        return self._local

    @local.setter
    def local(self, local):
        self._local = local

    def resolve(self, bot, clientid):
        try:
            name = self.name.resolve(bot, clientid)

            """
            Todo, if local then set per the conversation
            If globals
                If exists in predicates then don't replace
                If not in predicates then set as global to the conversation
            """

            if self.local is True:
                value = bot.get_conversation(clientid).current_question().predicate(name)
                if value is None:
                    logging.warning("No local var for %s, default-get used", name)
                    value = bot.brain.properties.property("default-get")
                    if value is None:
                        logging.error("No value for default-get defined, empty string returned")
                        value = ""
                logging.debug("[%s] resolved to local: [%s] <= [%s]", self.to_string(), name, value)
            else:
                value = bot.get_conversation(clientid).predicate(name)
                if value is None:
                    value = bot.brain.predicates.predicate(name)
                    if value is None:
                        value = bot.brain.properties.property("default-get")
                        if value is None:
                            logging.error("No value for default-get defined, empty string returned")
                            value = ""
                logging.debug("[%s] resolved to global: [%s] <= [%s]", self.to_string(), name, value)

            return value
        except Exception as excep:
            logging.exception(excep)
            return ""

    def to_string(self):
        return "[GET [%s] - %s]" % ("Local" if self.local else "Global", self.name.to_string())

    def output(self, tabs="", output=logging.debug):
        self.output_child(self, tabs, output)

    def to_xml(self, bot, clientid):
        xml = "<get"
        if self.local:
            xml += ' var="%s"' % self.name.resolve(bot, clientid)
        else:
            xml += ' name="%s"' % self.name.resolve(bot, clientid)
        xml += " />"
        return xml


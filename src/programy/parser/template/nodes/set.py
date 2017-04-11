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



class TemplateSetNode(TemplateNode):
    def __init__(self):
        TemplateNode.__init__(self)
        self._name = None
        self._local = True

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

    def resolve_children(self, bot, clientid):
        if len(self._children) > 0:
            return self.resolve_children_to_string(bot, clientid)
        else:
            return ""

    def resolve(self, bot, clientid):
        try:
            name = self.name.resolve(bot, clientid)
            value = self.resolve_children(bot, clientid)

            """
            #TODO, if local then set per the conversation
            If globals
                If exists in predicates then don't replace
                If not in predicates then set as global to the conversation
            """

            if self.local is True:
                logging.debug("[%s] resolved to local: [%s] => [%s]", self.to_string(), name, value)
                bot.get_conversation(clientid).current_question().set_predicate(name, value)
            else:
                if bot.override_predicates is False and bot.brain.properties.has_property(name):
                    logging.error("Global property already exists for name [%s], ignoring set!", name)
                    value = bot.brain.properties.property(name)
                else:
                    if bot.brain.properties.has_property(name):
                        logging.warning("Global property already exists for name [%s], over writing!", name)
                    logging.debug("[%s] resolved to global: [%s] => [%s]", self.to_string(), name, value)
                    bot.get_conversation(clientid).set_predicate(name, value)

            logging.debug("[%s] resolved to [%s]", self.to_string(), value)
            return value
        except Exception as excep:
            logging.exception(excep)
            return ""

    def to_string(self):
        return "[SET [%s] - %s]" % ("Local" if self.local else "Global", self.name.to_string())

    def to_xml(self, bot, clientid):
        xml = "<set"
        if self.local:
            xml += ' var="%s"' % self.name.resolve(None, None)
        else:
            xml += ' name="%s"' % self.name.resolve(None, None)
        xml += ">"
        for child in self.children:
            xml += child.to_xml(bot, clientid)
        xml += "</set>"
        return xml

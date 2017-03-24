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

from programy.parser.template.nodes.condition import TemplateConditionNode


class TemplateType1ConditionNode(TemplateConditionNode):

    def __init__(self, name, value, local=False):
        TemplateConditionNode.__init__(self)
        self._name = name
        self._value = value
        self._local = local

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def local(self):
        return self._local

    @local.setter
    def local(self, local):
        self._local = local

    def resolve(self, bot, clientid):
        value = self._get_predicate_value(bot, clientid, self.name, self.local)
        if value == self.value.resolve(bot, clientid):
            resolved = " ".join([child.resolve(bot, clientid) for child in self.children])
        else:
            resolved = ""

        logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        return "[CONDITION1(%s=%s)]" % (self.name, self.value)

    def to_xml(self, bot, clientid):
        xml = "<condition"
        if self.local is True:
            xml += ' var="%s"' % self.name
        else:
            xml += ' name="%s"' % self.name
        xml += ">"
        xml += '<value>'
        xml += self.value.to_xml(bot, clientid)
        xml += '</value>'
        for child in self.children:
            xml += child.to_xml(bot, clientid)
        xml += "</condition>"
        return xml

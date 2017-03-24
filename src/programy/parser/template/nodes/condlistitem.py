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

class TemplateConditionListItemNode(TemplateNode):

    def __init__(self, name=None, value=None, local=False, loop=False):
        TemplateNode.__init__(self)
        self._name = name
        self._value = value
        self._local = local
        self._loop = loop

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

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, loop):
        self._loop = loop

    def is_default(self):
        return bool(self.value is None)

    def resolve(self, bot, clientid):
        pass

    def to_string(self):
        return "[CONDITIONLIST(%s=%s)]" % (self.name, self.value)

    def to_xml(self, bot, clientid):
        xml = '<li'
        if self.name is not None:
            if self.local is True:
                xml += ' var="%s"' % self.name
            else:
                xml += ' name="%s"' % self.name
        xml += ">"
        if self.value is not None:
            xml += '<value>'
            xml += self.value.to_xml(bot, clientid)
            xml += '</value>'
        for child in self.children:
            xml += child.to_xml(bot, clientid)
        if self.loop is True:
            xml += "<loop />"
        xml += '</li>'
        return xml


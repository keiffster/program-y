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

from programy.parser.template.nodes.indexed import TemplateIndexedNode



######################################################################################################################
#
# <input index=”n”/> is replaced with the value of the nth previous sentence input to the bot.
#
class TemplateInputNode(TemplateIndexedNode):

    def __init__(self, position=1, index=1):
        TemplateIndexedNode.__init__(self, position, index)

    def resolve(self, bot, clientid):
        conversation = bot.get_conversation(clientid)
        sentence = conversation.nth_sentence(self.index)
        resolved = sentence
        logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        return "INPUT Index=%s" % (self.index)

    def to_xml(self, bot, clientid):
        xml = "<input"
        if self._position > 1:
            xml += ' position="%d"' % self._position
        if self._index > 1:
            xml += ' index="%d"' % self._index
        xml += ">"
        xml += "</input>"
        return xml

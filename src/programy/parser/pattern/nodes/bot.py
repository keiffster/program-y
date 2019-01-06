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
from programy.parser.pattern.nodes.base import PatternNode
from programy.parser.pattern.matcher import EqualsMatch
from programy.parser.exceptions import ParserException

class PatternBotNode(PatternNode):

    def __init__(self, attribs, text, userid='*'):
        PatternNode.__init__(self, userid)
        if 'name' in attribs:
            self._property = attribs['name']
        elif 'property' in attribs:
            self._property = attribs['property']
        elif text:
            self._property = text
        else:
            raise ParserException("Invalid bot node, neither name or property specified as attribute or text")

    def is_bot(self):
        return True

    @property
    def property(self):
        return self._property

    def to_xml(self, client_context, include_user=False):
        string = ""
        if include_user is True:
            string += '<bot userid="%s" property="%s">\n'%(self.userid, self.property)
        else:
            string += '<bot property="%s">\n' % self.property
        string += super(PatternBotNode, self).to_xml(client_context)
        string += "</bot>"
        return string

    def to_string(self, verbose=True):
        if verbose is True:
            return "BOT [%s] [%s] property=[%s]" % (self.userid, self._child_count(verbose), self.property)
        return "BOT property=[%s]" % (self.property)

    def equivalent(self, other):
        if other.is_bot():
            if self.userid == other.userid:
                if self.property == other.property:
                    return True
        return False

    def equals(self, client_context, words, word_no):
        word = words.word(word_no)

        if self.userid != '*':
            if self.userid != client_context.userid:
                return EqualsMatch(False, word_no)

        if client_context.brain.properties.has_property(self.property):
            if word == client_context.brain.properties.property(self.property):
                YLogger.debug(client_context, "Found word [%s] as bot property", word)
                return EqualsMatch(True, word_no, word)

        return EqualsMatch(False, word_no)

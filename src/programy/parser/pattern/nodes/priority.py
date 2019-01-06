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

from programy.parser.pattern.nodes.base import PatternNode
from programy.parser.pattern.matcher import EqualsMatch


class PatternPriorityWordNode(PatternNode):

    def __init__(self, word, userid='*'):
        PatternNode.__init__(self, userid)
        self._priority_word = word

    @property
    def priority_word(self):
        return self._priority_word

    def is_priority(self):
        return True

    def to_xml(self, client_context, include_user=False):
        string = ""
        if include_user is True:
            string += '<priority userid="%s" word="%s">'%(self.userid, self.priority_word)
        else:
            string += '<priority word="%s">'% self.priority_word
        string += super(PatternPriorityWordNode, self).to_xml(client_context)
        string += '</priority>\n'
        return string

    def to_string(self, verbose=True):
        if verbose is True:
            return "PWORD [%s] [%s] word=[%s]" % (self.userid, self._child_count(verbose), self.priority_word)
        return "PWORD [%s]" % (self.priority_word)

    def equivalent(self, other):
        if other.is_priority():
            if self.userid == other.userid:
                if self.priority_word == other.priority_word:
                    return True
        return False

    def equals(self, client_context, words, word_no):
        word = words.word(word_no)

        if self.userid != '*':
            if self.userid != client_context.userid:
                return EqualsMatch(False, word_no)

        if self.equals_ignore_case(self.priority_word, word):
            return EqualsMatch(True, word_no, word)

        return EqualsMatch(False, word_no)


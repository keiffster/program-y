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

from programy.parser.pattern.nodes.word import PatternWordNode


class PatternPriorityWordNode(PatternWordNode):

    def __init__(self, word):
        PatternWordNode.__init__(self, word)

    def is_priority(self):
        return True

    def equivalent(self, other):
        if isinstance(other, PatternPriorityWordNode):
            if self.word == other.word:
                return True
        return False

    def equals(self, bot, clientid, word):
        if self._word == word:
            return True
        return False

    def to_string(self, verbose=True):
        if verbose is True:
            return "PWORD [%s] word=[%s]" % (self._child_count(verbose), self.word)
        else:
            return "PWORD [%s]" % (self.word)

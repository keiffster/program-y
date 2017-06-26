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
from programy.parser.pattern.nodes.base import PatternNode
from programy.parser.pattern.matcher import EqualsMatch

class PatternBotNode(PatternNode):

    def __init__(self, property):
        PatternNode.__init__(self)
        self._property = property

    def is_bot(self):
        return True

    @property
    def property(self):
        return self._property

    def equivalent(self, other):
        if other.is_bot():
            if self.property == other.property:
                return True
        return False

    def equals(self, bot, clientid, words, word_no):
        word = words.word(word_no)
        if bot.brain.properties.has_property(self.property):
            if word == bot.brain.properties.property(self.property):
                logging.debug("Found word [%s] as bot property"%(word))
                return EqualsMatch(True, word_no, word)
        return EqualsMatch(False, word_no)

    def to_string(self, verbose=True):
        if verbose is True:
            return "BOT [%s] property=[%s]" % (self._child_count(verbose), self.property)
        else:
            return "BOT property=[%s]" % (self.property)

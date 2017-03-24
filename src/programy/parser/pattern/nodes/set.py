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


class PatternSetNode(PatternWordNode):

    def __init__(self, word):
        PatternWordNode.__init__(self, word.upper())

    @property
    def set_name(self):
        return self.word

    def is_set(self):
        return True

    def equivalent(self, other):
        if isinstance(other, PatternSetNode):
            if self._word == other.word:
                return True
        return False

    def equals(self, bot, client, word):
        if self.set_name.upper() == 'NUMBER':
            return word.isnumeric()
        elif bot.brain.sets.contains(self.set_name):
            logging.debug("Looking for [%s] in set [%s]", word, self.set_name)
            set_words = bot.brain.sets.set(self.set_name)
            if word in set_words:
                logging.debug("Found word [%s] in set [%s]"%(word, self.set_name))
                return True
        return False

    def to_string(self, verbose=True):
        if verbose is True:
            return "SET [%s] name=[%s]" % (self._child_count(verbose), self.word)
        else:
            return "SET name=[%s]" % (self.word)


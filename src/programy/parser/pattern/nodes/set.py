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

class PatternSetNode(PatternNode):

    def __init__(self, name):
        PatternNode.__init__(self)
        self._set_name = name.upper()

    @property
    def set_name(self):
        return self._set_name

    def is_set(self):
        return True

    def equivalent(self, other):
        if other.is_set():
            if self.set_name == other.set_name:
                return True
        return False

    def set_is_numeric(self):
        return bool(self.set_name.upper() == 'NUMBER')

    def set_is_known(self, bot):
        return bool(bot.brain.sets.contains(self.set_name))

    def words_in_set(self, bot, words, word_no):

        word = words.word(word_no).upper()
        set_words = bot.brain.sets.set(self.set_name)

        if word in set_words:
            phrases = set_words[word]
            phrases = sorted(phrases, key=len, reverse=True)
            for phrase in phrases:
                phrase_word_no = 0
                words_word_no = word_no
                while phrase_word_no < len(phrase) and words_word_no < words.num_words():
                    phrase_word = phrase[phrase_word_no].upper()
                    word = words.word(words_word_no).upper()
                    if phrase_word == word:
                        if phrase_word_no+1 == len(phrase):
                            return EqualsMatch(True, words_word_no, " ".join(phrase))
                    phrase_word_no += 1
                    words_word_no += 1

        return EqualsMatch(False, word_no)

    def equals(self, bot, client, words, word_no):
        word = words.word(word_no)

        if self.set_is_numeric():
            return EqualsMatch(word.isnumeric(), word_no, word)
        elif self.set_is_known(bot):
            match = self.words_in_set(bot, words, word_no)
            if match.matched is True:
                logging.debug("Found word [%s] in set [%s]"%(word, self.set_name))
                return match
            else:
                logging.error("No word [%s] found in set [%s]"%(word, self.set_name))
                return EqualsMatch(False, word_no)
        else:
            logging.error("No set named [%s] in sets collection"%(self.set_name))
            return EqualsMatch(False, word_no)

    def to_string(self, verbose=True):
        if verbose is True:
            return "SET [%s] name=[%s]" % (self._child_count(verbose), self.set_name)
        else:
            return "SET name=[%s]" % (self.set_name)


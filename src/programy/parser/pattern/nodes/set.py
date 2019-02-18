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

class PatternSetNode(PatternNode):

    def __init__(self, attribs, text, userid='*'):
        PatternNode.__init__(self, userid)
        if 'name' in attribs:
            self._set_name = attribs['name'].upper()
        elif text:
            self._set_name = text.upper()
        else:
            raise ParserException("Invalid set node, no name specified as attribute or text")

    @property
    def set_name(self):
        return self._set_name

    def is_set(self):
        return True

    def to_xml(self, client_context, include_user=False):
        string = ""
        if include_user is True:
            string += '<set userid="%s" name="%s">\n'%(self.userid, self.set_name)
        else:
            string += '<set name="%s">\n' % self.set_name
        string += super(PatternSetNode, self).to_xml(client_context)
        string += "</set>"
        return string

    def to_string(self, verbose=True):
        if verbose is True:
            return "SET [%s] [%s] name=[%s]" % (self.userid, self._child_count(verbose), self.set_name)
        return "SET name=[%s]" % (self.set_name)

    def set_is_numeric(self):
        return bool(self.set_name.upper() == 'NUMBER')

    def set_is_known(self, client_context):
        return bool(client_context.brain.sets.contains(self.set_name))

    def words_in_set(self, client_context, words, word_no):

        word = words.word(word_no).upper()
        set_words = client_context.brain.sets.set(self.set_name)
        if not set_words:
            YLogger.error(self, "No set with name [%s]", self.set_name)

        elif word in set_words:
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

    def equivalent(self, other):
        if other.is_set():
            if self.userid == other.userid:
                if self.set_name == other.set_name:
                    return True
        return False

    def equals(self, client_context, words, word_no):
        word = words.word(word_no)

        if self.userid != '*':
            if self.userid != client_context.userid:
                return EqualsMatch(False, word_no)

        if client_context.brain.dynamics.is_dynamic_set(self._set_name) is True:
            result = client_context.brain.dynamics.dynamic_set(client_context, self._set_name, word)
            return EqualsMatch(result, word_no, word)
        else:
            if self.set_is_known(client_context):
                match = self.words_in_set(client_context, words, word_no)
                if match.matched is True:
                    YLogger.debug(client_context, "Found word [%s] in set [%s]", word, self.set_name)
                    return match
                else:
                    YLogger.error(client_context, "No word [%s] found in set [%s]", word, self.set_name)
                    return EqualsMatch(False, word_no)
            else:
                YLogger.error(client_context, "No set named [%s] in sets collection", self.set_name)
                return EqualsMatch(False, word_no)


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


class PatternISetNode(PatternNode):

    iset_count = 1

    def __init__(self, attribs, text, userid='*'):
        PatternNode.__init__(self, userid)
        self._words = []

        if 'words' in attribs:
            words = attribs['words'].upper()
        elif text:
            words = text.upper()
        else:
            raise ParserException("Invalid iset node, no words specified as attribute or text")

        self._parse_words(words)
        self._iset_name = "iset_%d"%(PatternISetNode.iset_count)
        PatternISetNode.iset_count += 1

    def _parse_words(self, words):
        splits = words.split(",")
        for word in splits:
            self._words.append(word.strip().upper())

    @property
    def words(self):
        return self._words

    @property
    def iset_name(self):
        return self._iset_name

    def is_iset(self):
        return True

    def to_xml(self, client_context, include_user=False):
        string = ""
        if include_user is True:
            string += '<iset userid="%s" words="%s">'%(self.userid, ". ".join(self.words))
        else:
            string += '<iset words="%s">'% ". ".join(self.words)
        string += super(PatternISetNode, self).to_xml(client_context)
        string += "</iset>\n"
        return string

    def to_string(self, verbose=True):
        words_str = ",".join(self._words)
        if verbose is True:
            return "ISET [%s] [%s] words=[%s]" % (self.userid, self._child_count(verbose), words_str)
        return "ISET words=[%s]" % words_str

    def equivalent(self, other):
        if self.userid != other.userid:
            return False

        for word in self.words:
            if word not in other.words:
                return False

        return True

    def equals(self, client_context, words, word_no):
        if self.userid != '*':
            if self.userid != client_context.userid:
                return EqualsMatch(False, word_no)

        word = words.word(word_no)
        if word is not None:
            word = word.upper()
            for set_word in self._words:
                if word == set_word:
                    YLogger.debug(client_context, "Found word [%s] in iset", word)
                    return EqualsMatch(True, word_no, word)

        YLogger.error(client_context, "No word [%s] found in iset", word)
        return EqualsMatch(False, word_no)

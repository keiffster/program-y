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
from programy.dialog import Sentence


class Match(object):

    WORD = 0
    TOPIC = 2
    THAT = 3

    def __init__(self, type, node, word):
        self._match_type = type
        self._matched_node = node
        self._matched_words = []
        if word is not None:
            self.add_word(word)

    def add_word(self, word):
        self._matched_words.append(word)

    @property
    def match_type(self):
        return self._match_type

    @property
    def matched_node(self):
        return self._matched_node

    @property
    def matched_words(self):
        return self._matched_words

    def joined_words(self, join_char=" "):
        return join_char.join(self.matched_words)

    @staticmethod
    def type_to_string(type):
        if type == Match.WORD:
            return "Word"
        elif type == Match.TOPIC:
            return "Topic"
        elif type == Match.THAT:
            return "That"
        else:
            return "Unknown"

    def to_string(self):
        return "Match=(%s) Node=(%s) Matched=(%s)"%(Match.type_to_string(self._match_type), self._matched_node.to_string(verbose=False), self.joined_words())


class MatchContext(object):

    MAX_SEARCH_DEPTH = 10000

    def __init__(self, max_search_depth=MAX_SEARCH_DEPTH):
        self._matched_nodes = []
        self._template_node = None
        self._max_search_depth = max_search_depth

    @property
    def max_search_depth(self):
        return self._max_search_depth

    def add_match(self, match):
        self._matched_nodes.append(match)

    def pop_match(self):
        if len(self._matched_nodes) > 0:
            self._matched_nodes.pop()

    def pop_matches(self, matches_add):
        for x in range(0, matches_add):
            self.pop_match()

    def set_template(self, template):
        self._template_node = template

    @property
    def matched_nodes(self):
        return self._matched_nodes

    def template_node(self):
        return self._template_node

    def matched(self):
        if self._template_node is not None:
            return True
        else:
            return False

    def _get_indexed_match_by_type(self, index, type):
        count = 1
        for match in self._matched_nodes:
            if match._match_type == type and \
                ( match._matched_node.is_wildcard() or
                  match._matched_node.is_set() or
                  match._matched_node.is_bot()):
                if count == index:
                    return match.joined_words()
                count += 1
        return None

    def star(self, index):
        return self._get_indexed_match_by_type(index,  Match.WORD)

    def topicstar(self, index):
        return self._get_indexed_match_by_type(index,  Match.TOPIC)

    def thatstar(self, index):
        return self._get_indexed_match_by_type(index,  Match.THAT)

    def list_matches(self, output_func=logging.debug):
        output_func("Matches...")
        count = 1
        for match in self._matched_nodes:
            output_func("\t%d - %s"%(count, match.to_string()))
            count += 1
        if self.matched() is True:
            output_func("\tT - %s"%(self._template_node.to_string()))
        else:
            output_func("\tT - None")


class EqualsMatch(object):
    def __init__(self, matched, word_no, matched_phrase=None):
        self._matched = matched
        self._word_no = word_no
        self._matched_phrase = matched_phrase

    @property
    def matched(self):
        return self._matched

    @property
    def word_no(self):
        return self._word_no

    @property
    def matched_phrase(self):
        return self._matched_phrase

    def to_string(self):
        return "%s, %d, %s"%(self._matched, self._word_no, self.matched_phrase)
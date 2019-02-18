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
import datetime

class Match(object):

    WORD = 0
    TOPIC = 2
    THAT = 3

    def __init__(self, match_type, node, word):
        self._match_type = match_type
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

    def joined_words(self, tokenizer):
        return tokenizer.words_to_texts(self.matched_words)

    @staticmethod
    def type_to_string(match_type):
        if match_type == Match.WORD:
            return "Word"
        elif match_type == Match.TOPIC:
            return "Topic"
        elif match_type == Match.THAT:
            return "That"
        return "Unknown"

    def to_string(self, tokenizer):
        return "Match=(%s) Node=(%s) Matched=(%s)"%(Match.type_to_string(self._match_type),
                                                    self._matched_node.to_string(verbose=False),
                                                    self.joined_words(tokenizer))


class MatchContext(object):

    def __init__(self, max_search_depth, max_search_timeout, tokenizer):
        self._tokenizer = tokenizer
        self._matched_nodes = []
        self._template_node = None
        self._max_search_depth = max_search_depth
        self._max_search_timeout = max_search_timeout
        self._total_search_start = datetime.datetime.now()

    @property
    def max_search_depth(self):
        return self._max_search_depth

    def search_depth_exceeded(self, depth):
        if self._max_search_depth == -1:
            return False
        return bool(depth > self._max_search_depth)

    @property
    def max_search_timeout(self):
        return self._max_search_timeout

    def total_search_time(self):
        delta = datetime.datetime.now() - self._total_search_start
        return abs(delta.total_seconds())

    def search_time_exceeded(self):
        if self._max_search_timeout == -1:
            return False
        return bool(self.total_search_time() >= self._max_search_timeout)

    def add_match(self, match):
        self._matched_nodes.append(match)

    def pop_match(self):
        if self._matched_nodes:
            self._matched_nodes.pop()

    def pop_matches(self, matches_add):
        for match in range(0, matches_add):
            self.pop_match()

    def set_template(self, template):
        self._template_node = template

    @property
    def matched_nodes(self):
        return self._matched_nodes

    def template_node(self):
        return self._template_node

    def matched(self):
        return bool(self._template_node is not None)

    def _get_indexed_match_by_type(self, index, match_type):
        count = 1
        for match in self._matched_nodes:
            if match.match_type == match_type and \
                    (match.matched_node.is_wildcard() or
                     match.matched_node.is_set() or
                     match.matched_node.is_iset() or
                     match.matched_node.is_bot() or
                     match.matched_node.is_regex()):
                if count == index:
                    return match.joined_words(self._tokenizer)
                count += 1
        return None

    def star(self, index):
        return self._get_indexed_match_by_type(index, Match.WORD)

    def topicstar(self, index):
        return self._get_indexed_match_by_type(index, Match.TOPIC)

    def thatstar(self, index):
        return self._get_indexed_match_by_type(index, Match.THAT)

    def list_matches(self, client_context, output_func=YLogger.debug, tabs="\t", include_template=True):
        output_func(client_context, "%sMatches..."%tabs)
        count = 1
        for match in self._matched_nodes:
            output_func(client_context, "%s\t%d - %s"%(tabs, count, match.to_string(self._tokenizer)))
            count += 1
        output_func(client_context, "%sMatch score %.2f"%(tabs, self.calculate_match_score()))
        if include_template is True:
            if self.matched() is True:
                output_func(client_context, "%s\tT - %s"%(tabs, self._template_node.to_string()))
            else:
                output_func(client_context, "%s\tT - None"%tabs)

    def calculate_match_score(self):
        wildcards = 0
        words = 0
        for match in self._matched_nodes:
            if match.match_type == Match.WORD:
                if match.matched_node.is_wildcard():
                    wildcards += 1
                else:
                    words += 1
        total = wildcards+words
        if total > 0:
            return (words/(wildcards+words))*100.00
        return 0.00

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

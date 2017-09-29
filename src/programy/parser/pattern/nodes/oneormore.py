"""
Copyright (c) 2016-17 Keith Sterling http://www.keithsterling.com

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

import logging

from programy.parser.pattern.nodes.wildcard import PatternWildCardNode
from programy.parser.pattern.matcher import Match
from programy.parser.pattern.nodes.base import PatternNode

class PatternOneOrMoreWildCardNode(PatternWildCardNode):

    MATCH_CHARS = ['_', '*']

    def __init__(self, wildcard):
        PatternWildCardNode.__init__(self, wildcard)

    def is_one_or_more(self):
        return True

    def matching_wildcards(self):
        return PatternOneOrMoreWildCardNode.MATCH_CHARS

    def to_xml(self, bot, clientid):
        string = ""
        string += '<oneormore wildcard="%s">\n' % self.wildcard
        string += super(PatternOneOrMoreWildCardNode, self).to_xml(bot, clientid)
        string += "</oneormore>\n"
        return string

    @staticmethod
    def is_wild_card(text):
        return bool(text in PatternOneOrMoreWildCardNode.MATCH_CHARS)

    def equivalent(self, other):
        if other.is_one_or_more():
            if self._wildcard == other.wildcard:
                return True
        return False

    def to_string(self, verbose=True):
        if verbose is True:
            return "ONEORMORE [%s] wildcard=[%s]" % (self._child_count(verbose), self.wildcard)
        return "ONEORMORE [%s]" % (self.wildcard)

    def consume(self, bot, clientid, context, words, word_no, match_type, depth):

        tabs = self.get_tabs(bot, depth)

        if context.search_time_exceeded() is True:
            if logging.getLogger().isEnabledFor(logging.ERROR):
                logging.error("%sMax search time [%d]secs exceeded", tabs, context.max_search_timeout)
            return None

        if context.search_depth_exceeded(depth) is True:
            if logging.getLogger().isEnabledFor(logging.ERROR):
                logging.error("%sMax search depth [%d] exceeded", tabs, context.max_search_depth)
            return None

        if word_no >= words.num_words():
            return None

        word = words.word(word_no)
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("%sWildcard %s matched %s", tabs, self._wildcard, word)
        context_match = Match(match_type, self, word)
        context.add_match(context_match)
        matches_added = 1

        match = self.check_child_is_wildcard(tabs, bot, clientid, context, words, word_no, match_type, depth)
        if match is not None:
            return match

        if self._topic is not None:
            match = self._topic.consume(bot, clientid, context, words, word_no+1, Match.TOPIC, depth+1)
            if match is not None:
                if logging.getLogger().isEnabledFor(logging.DEBUG):
                    logging.debug("%sMatched topic, success!", tabs)
                return match
            if words.word(word_no) == PatternNode.TOPIC:
                if logging.getLogger().isEnabledFor(logging.DEBUG):
                    logging.debug("%s Looking for a %s, none give, no match found!", tabs, PatternNode.TOPIC)
                return None

        if self._that is not None:
            match = self._that.consume(bot, clientid, context, words, word_no+1, Match.THAT, depth+1)
            if match is not None:
                if logging.getLogger().isEnabledFor(logging.DEBUG):
                    logging.debug("%sMatched that, success!", tabs)
                return match
            if words.word(word_no) == PatternNode.THAT:
                if logging.getLogger().isEnabledFor(logging.DEBUG):
                    logging.debug("%s Looking for a %s, none give, no match found!", tabs, PatternNode.THAT)
                return None

        word_no += 1
        if word_no >= words.num_words():
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("%sNo more words", tabs)
            return super(PatternOneOrMoreWildCardNode, self).consume(bot,
                                                                     clientid, context, words, word_no, match_type, depth+1)
        word = words.word(word_no)

        if self._children:
            for child in self._children:

                result = child.equals(bot, clientid, words, word_no)
                if result.matched is True:
                    word_no = result.word_no
                    if logging.getLogger().isEnabledFor(logging.DEBUG):
                        logging.debug("%sWildcard child matched %s", tabs, result.matched_phrase)

                    context_match2 = Match(Match.WORD, child, result.matched_phrase)

                    context.add_match(context_match2)
                    matches_added += 1

                    match = child.consume(bot, clientid, context, words, word_no+1, match_type, depth+1)
                    if match is not None:
                        return match

            if self.invalid_topic_or_that(tabs, word, context, matches_added) is True:
                return None

            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("%sWildcard %s matched %s", tabs, self._wildcard, word)
            context_match.add_word(word)

            word_no += 1
            if word_no >= words.num_words():
                context.pop_matches(matches_added)
                return None
            word = words.word(word_no)

        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("%sNo children, consume words until next break point", tabs)

        while word_no < words.num_words()-1:
            match = super(PatternOneOrMoreWildCardNode, self).consume(bot, clientid, context, words, word_no, match_type, depth+1)
            if match is not None:
                return match

            if self.invalid_topic_or_that(tabs, word, context, matches_added) is True:
                return None

            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("%sWildcard %s matched %s", tabs, self._wildcard, word)
            context_match.add_word(word)

            word_no += 1
            word = words.word(word_no)

        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("%sWildcard %s matched %s", tabs, self._wildcard, word)
        context_match.add_word(word)

        if word_no == words.num_words()-1:
            match = super(PatternOneOrMoreWildCardNode, self).consume(bot, clientid, context, words, word_no+1, match_type, depth+1)
        else:
            match = super(PatternOneOrMoreWildCardNode, self).consume(bot, clientid, context, words, word_no, match_type, depth+1)

        if match is not None:
            return match
        context.pop_matches(matches_added)
        return None

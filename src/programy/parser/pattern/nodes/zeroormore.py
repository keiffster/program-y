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

from programy.parser.pattern.nodes.wildcard import PatternWildCardNode
from programy.parser.pattern.matcher import Match
from programy.parser.pattern.nodes.base import PatternNode


class PatternZeroOrMoreWildCardNode(PatternWildCardNode):

    MATCH_CHARS = ['^', '#']

    def __init__(self, wildcard, userid='*'):
        PatternWildCardNode.__init__(self, wildcard, userid)

    def is_zero_or_more(self):
        return True

    def matching_wildcards(self):
        return PatternZeroOrMoreWildCardNode.MATCH_CHARS

    @staticmethod
    def is_wild_card(text):
        return bool(text in PatternZeroOrMoreWildCardNode.MATCH_CHARS)

    def to_xml(self, client_context, include_user=False):
        string = ""
        if include_user is True:
            string += '<zerormore userid="%s" wildcard="%s">\n'%(self.userid, self.wildcard)
        else:
            string += '<zerormore wildcard="%s">\n' % self.wildcard
        string += super(PatternZeroOrMoreWildCardNode, self).to_xml(client_context)
        string += "</zerormore>\n"
        return string

    def to_string(self, verbose=True):
        if verbose is True:
            return "ZEROORMORE [%s] [%s] wildcard=[%s]" % (self.userid, self._child_count(verbose), self.wildcard)
        return "ZEROORMORE [%s]" % (self.wildcard)

    def equivalent(self, other):
        if other.is_zero_or_more():
            if self.userid == other.userid:
                if self._wildcard == other.wildcard:
                    return True
        return False

    def consume(self, client_context, context, words, word_no, match_type, depth, parent_wildcard=False):

        tabs = self.get_tabs(client_context, depth)

        if context.search_time_exceeded() is True:
            YLogger.error(client_context, "%sMax search time [%d]secs exceeded", tabs, context.max_search_timeout)
            return None

        if context.search_depth_exceeded(depth) is True:
            YLogger.error(client_context, "%sMax search depth [%d] exceeded", tabs, context.max_search_depth)
            return None

        context_match = Match(match_type, self, None)
        context.add_match(context_match)
        matches_added = 1

        match = self.check_child_is_wildcard(tabs, client_context, context, words, word_no, match_type, depth)
        if match is not None:
            return match

        if self._topic is not None:
            match = self._topic.consume(client_context, context, words, word_no, Match.TOPIC, depth+1)

            if match is not None:
                YLogger.debug(client_context, "%sMatched topic, success!", tabs)
                return match

            if words.word(word_no) == PatternNode.TOPIC:
                YLogger.debug(client_context, "%s Looking for a %s, none given, no match found!", tabs, PatternNode.TOPIC)
                context.pop_matches(matches_added)
                return None

        word = words.word(word_no)

        if self._priority_words or self._children:

            ################################################################################################################
            # Priority nodes
            for child in self._priority_words:

                result = child.equals(client_context, words, word_no)
                if result.matched is True:
                    word_no = result.word_no
                    YLogger.debug(client_context, "%sWildcard child matched %s", tabs, result.matched_phrase)

                    context_match2 = Match(Match.WORD, child, result.matched_phrase)

                    context.add_match(context_match2)
                    matches_added += 1

                    match = child.consume(client_context, context, words, word_no + 1, match_type, depth + 1)
                    if match is not None:
                        return match

                    if self.invalid_topic_or_that(tabs, client_context, word, context, matches_added) is True:
                        context.pop_matches(matches_added)
                        return None

            ################################################################################################################
            # Children nodes
            for child in self._children:

                result = child.equals(client_context, words, word_no)
                if result.matched is True:
                    word_no = result.word_no
                    YLogger.debug(client_context, "%sWildcard child matched %s", tabs, result.matched_phrase)

                    context_match2 = Match(Match.WORD, child, result.matched_phrase)

                    context.add_match(context_match2)
                    matches_added += 1

                    match = child.consume(client_context, context, words, word_no+1, match_type, depth+1)
                    if match is not None:
                        return match

                    if self.invalid_topic_or_that(tabs, client_context, word, context, matches_added) is True:
                        context.pop_matches(matches_added)
                        return None

            YLogger.debug(client_context, "%sWildcard %s matched %s", tabs, self._wildcard, word)
            context_match.add_word(word)

            match = super(PatternZeroOrMoreWildCardNode, self).consume(client_context, context, words, word_no + 1, match_type, depth+1)
            if match is not None:
                return match

            word_no += 1
            word = words.word(word_no)

            if self.invalid_topic_or_that(tabs, client_context, word, context, matches_added) is True:
                context.pop_matches(matches_added)
                return None

            YLogger.debug(client_context, "%sWildcard %s matched %s", tabs, self._wildcard, word)
            context_match.add_word(word)

            match = super(PatternZeroOrMoreWildCardNode, self).consume(client_context, context, words, word_no + 1, match_type, depth+1)
            if match is not None:
                return match

            word_no += 1
            if word_no >= words.num_words():
                context.pop_matches(matches_added)
                return None
            word = words.word(word_no)

        YLogger.debug(client_context, "%sNo children, consume words until next break point", tabs)

        while word_no < words.num_words() - 1:
            match = super(PatternZeroOrMoreWildCardNode, self).consume(client_context, context, words, word_no, match_type, depth+1)
            if match is not None:
                return match

            if self.invalid_topic_or_that(tabs, client_context, word, context, matches_added) is True:
                context.pop_matches(matches_added)
                return None

            YLogger.debug(client_context, "%sWildcard %s matched %s", tabs, self._wildcard, word)
            context_match.add_word(word)

            word_no += 1
            word = words.word(word_no)

        if parent_wildcard is True:
            match = super(PatternZeroOrMoreWildCardNode, self).consume(client_context, context, words, word_no+1, match_type,
                                                                       depth + 1)
        else:
            match = super(PatternZeroOrMoreWildCardNode, self).consume(client_context, context, words, word_no, match_type,
                                                                       depth + 1)
        if match is not None:
            return match

        context.pop_matches(matches_added)
        return None

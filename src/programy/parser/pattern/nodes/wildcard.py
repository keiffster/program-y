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

from programy.parser.exceptions import ParserException
from programy.parser.pattern.nodes.base import PatternNode
from programy.parser.pattern.nodes.topic import PatternTopicNode
from programy.parser.pattern.nodes.that import PatternThatNode


class PatternWildCardNode(PatternNode):

    def __init__(self, wildcard, userid='*'):
        PatternNode.__init__(self, userid)
        if wildcard not in self.matching_wildcards():
            raise ParserException("%s not in valid wildcards %s" % (wildcard, ", ".join(self.matching_wildcards())))
        self._wildcard = wildcard

    def is_wildcard(self):
        return True

    def can_add(self, new_node):
        if new_node.is_root():
            raise ParserException("Cannot add root node to child node")

    @property
    def wildcard(self):
        return self._wildcard

    def matching_wildcards(self):
        return []

    def invalid_topic_or_that(self, tabs, client_context, word, context, matches_add):
        if word == PatternTopicNode.TOPIC:
            YLogger.debug(client_context, "%sFound a topic at the wrong place....", tabs)
            context.pop_matches(matches_add)
            return True

        if word == PatternThatNode.THAT:
            YLogger.debug(client_context, "%sFound a that at the wrong place....", tabs)
            context.pop_matches(matches_add)
            return True

        return False

    def check_child_is_wildcard(self, tabs, client_context, context, words, word_no, match_type, depth):
        if self._0ormore_hash is not None:
            YLogger.debug(client_context, "%sWildcard # is next node, moving on!", tabs)
            match = self._0ormore_hash.consume(client_context, context, words, word_no+1, match_type, depth+1, parent_wildcard=True)
            if match is not None:
                return match

        if self._1ormore_underline is not None:
            YLogger.debug(client_context, "%sWildcard _ is next node, moving on!", tabs)
            match = self._1ormore_underline.consume(client_context, context, words, word_no+1, match_type, depth+1)
            if match is not None:
                return match

        if self._0ormore_arrow is not None:
            YLogger.debug(client_context, "%sWildcard ^ is next node, moving on!", tabs)
            match = self._0ormore_arrow.consume(client_context, context, words, word_no+1, match_type, depth+1, parent_wildcard=True)
            if match is not None:
                return match

        if self._1ormore_star is not None:
            YLogger.debug(client_context, "%sWildcard * is next node, moving on!", tabs)
            match = self._1ormore_star.consume(client_context, context, words, word_no+1, match_type, depth+1)
            if match is not None:
                return match

        return None

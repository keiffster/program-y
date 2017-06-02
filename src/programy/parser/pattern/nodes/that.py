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

from programy.utils.text.text import TextUtils

from programy.parser.exceptions import ParserException
from programy.parser.pattern.nodes.base import PatternNode


class PatternThatNode(PatternNode):

    def __init__(self):
        PatternNode.__init__(self)

    def can_add(self, new_node):
        if new_node.is_root():
            raise ParserException("Cannot add root node to that node")
        if new_node.is_topic():
            raise ParserException("Cannot add topic node to that node")
        if new_node.is_that():
            raise ParserException("Cannot add that node to that node")

    def is_that(self):
        return True

    def equivalent(self, other):
        if other.is_that():
            return True
        return False

    def to_string(self, verbose=True):
        if verbose is True:
            return "THAT [%s]" % self._child_count(verbose)
        else:
            return "THAT"

    def consume(self, bot, clientid, context, words, word_no, type, depth):

        tabs = TextUtils.get_tabs(word_no)

        if depth > context.max_search_depth:
            logging.error("%sMax search depth [%d]exceeded" % (tabs, context.max_search_depth))
            return None

        if words.word(word_no) == PatternThatNode.THAT:
            logging.debug("%sThat matched %s" % (tabs, words.word(word_no)))
            return super(PatternThatNode, self).consume(bot, clientid, context, words, word_no + 1, type, depth+1)

        logging.debug("%sTHAT NOT matched %s" % (tabs, words.word(word_no)))
        return None

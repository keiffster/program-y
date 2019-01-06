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


class PatternThatNode(PatternNode):

    def __init__(self, userid='*'):
        PatternNode.__init__(self, userid)

    def is_that(self):
        return True

    def to_xml(self, client_context, include_user=False):
        string = ""
        if include_user is True:
            string += '<that userid="%s">'%self.userid
        else:
            string += '<that>'
        string += super(PatternThatNode, self).to_xml(client_context)
        string += '</that>\n'
        return string

    def to_string(self, verbose=True):
        if verbose is True:
            return "THAT [%s] [%s]" % (self.userid, self._child_count(verbose))
        return "THAT"

    def can_add(self, new_node):
        if new_node.is_root():
            raise ParserException("Cannot add root node to that node")
        if new_node.is_topic():
            raise ParserException("Cannot add topic node to that node")
        if new_node.is_that():
            raise ParserException("Cannot add that node to that node")

    def equivalent(self, other):
        if other.is_that():
            if self.userid == other.userid:
                return True
        return False

    def consume(self, client_context, context, words, word_no, match_type, depth):

        tabs = self.get_tabs(client_context, depth)

        if context.search_depth_exceeded(depth) is True:
            YLogger.error(client_context, "%sMax search depth [%d]exceeded", tabs, context.max_search_depth)
            return None

        if words.word(word_no) == PatternThatNode.THAT:
            YLogger.debug(client_context, "%sThat matched %s", tabs, words.word(word_no))
            return super(PatternThatNode, self).consume(client_context, context, words, word_no + 1, match_type, depth+1)

        YLogger.debug(client_context, "%sTHAT NOT matched %s", tabs, words.word(word_no))
        return None

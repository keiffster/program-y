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

from programy.parser.exceptions import ParserException
from programy.parser.pattern.nodes.base import PatternNode


class PatternTemplateNode(PatternNode):

    def __init__(self, template, userid='*'):
        PatternNode.__init__(self, userid)
        self._template = template

    @property
    def template(self):
        return self._template

    def is_template(self):
        return True

    def can_add(self, new_node):
        if new_node.is_root():
            raise ParserException("Cannot add root node to template node")
        elif new_node.is_topic():
            raise ParserException("Cannot add topic node to template node")
        elif new_node.is_that():
            raise ParserException("Cannot add that node to template node")
        elif new_node.is_template():
            raise ParserException("Cannot add template node to template node")

    def to_xml(self, client_context, include_user=False):
        string = ""
        if include_user is True:
            string += '<template userid="%s">'%self.userid
        else:
            string += '<template>'
        string2 = super(PatternTemplateNode, self).to_xml(client_context, include_user)
        string += string2
        string += '</template>\n'
        return string

    def to_string(self, verbose=True):
        if verbose is True:
            return "PTEMPLATE [%s] [%s]" %(self.userid, self._child_count(verbose))
        return "PTEMPLATE"

    def equivalent(self, other):
        if other.is_template():
            if self.userid == other.userid:
                return True
        return False


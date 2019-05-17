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
from programy.parser.template.nodes.attrib import TemplateAttribNode
from programy.parser.template.nodes.word import TemplateWordNode


class TemplateIndexedNode(TemplateAttribNode):

    def __init__(self, index=1):
        TemplateAttribNode.__init__(self)
        self._index = TemplateWordNode(str(index))

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        self._index = TemplateWordNode(str(value))

    def resolve_children_to_string(self, client_context):
        raise NotImplementedError()

    def resolve_to_string(self, client_context):
        raise NotImplementedError()

    def set_attrib(self, attrib_name, attrib_value):

        if attrib_name != 'index':
            raise ParserException("Invalid attribute name [%s] for this node" % (attrib_name))

        if isinstance(attrib_value, TemplateWordNode):
            splits = attrib_value.word.split(",")
            if len(splits) == 1:
                if splits[0].isnumeric() is False:
                    raise ParserException("None numeric format [%s] for this node [%s]", attrib_value, attrib_name)
            elif len(splits) == 2:
                if splits[0].strip().isnumeric() is False:
                    raise ParserException("None numeric format [%s] for this node [%s] either num or num,num",
                                          attrib_value, attrib_name)
                splits1 = splits[1].strip()
                if splits1 != '*' and splits1.isnumeric() is False:
                    raise ParserException("None numeric format [%s] for this node [%s] either num or num,num",
                                          attrib_value, attrib_name)

            else:
                raise ParserException("None numeric format [%s] for this node [%s] either num or num,num",
                                      attrib_value, attrib_name)

        self._index = attrib_value

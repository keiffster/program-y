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

from programy.parser.exceptions import ParserException
from programy.parser.template.nodes.atttrib import TemplateAttribNode


######################################################################################################################
#
class TemplateIndexedNode(TemplateAttribNode):

    def __init__(self, position=1, index=1):
        TemplateAttribNode.__init__(self)
        # TODO Position means question
        # Index means setence in question
        # Need to make sure every index class is using this correctly
        # See TODO Below
        self._position = position
        self._index = index

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, index):
        self._index = index

    def set_attrib(self, attrib_name, attrib_value):

        if attrib_name != 'index':
            raise ParserException("Invalid attribute name [%s] for this node" % (attrib_name))

        if isinstance(attrib_value, int):
            int_val = attrib_value
            self._index = int_val
        else:
            splits = attrib_value.split(",")
            if len(splits) == 1:
                try:
                    self._index = int(splits[0])
                except Exception as excep:
                    logging.exception(excep)
                    raise ParserException("None numeric format [%s] for this node [%s], either 'x' or 'x,y'", attrib_value, attrib_name)
            elif len(splits) == 2:
                try:
                    self._position = int(splits[0])
                    if splits[1] == '*':
                        # TODO I think this is wrong
                        # A number of aiml files use index="2,*", where * means all sentences
                        self._index = 1
                    else:
                        self._index = int(splits[1])
                except Exception as excep:
                    logging.exception(excep)
                    raise ParserException("None numeric format [%s] for this node [%s], either 'x' or 'x,y'", attrib_value, attrib_name)

        if self._index == 0:
            raise ParserException("Index values are 1 based, cannot be 0")
        if self._position == 0:
            raise ParserException("Position values are 1 based, cannot be 0")


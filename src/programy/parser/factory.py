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
import os
from abc import ABCMeta, abstractmethod

from programy.utils.classes.loader import ClassLoader

class NodeFactory(object):
    __metaclass__ = ABCMeta

    def __init__(self, node_type):
        self._nodes_config = {}
        self._type = node_type

    @property
    def type(self):
        return self._type

    @property
    def nodes(self):
        return self._nodes_config

    def empty(self):
        self._nodes_config.clear()

    @abstractmethod
    def default_config_file(self):
        raise NotImplementedError()

    def add_node(self, name, instance):
        self._nodes_config[name] = instance

    def exists(self, node_name):
        return node_name in self._nodes_config

    def new_node_class(self, name):
        if name not in self._nodes_config:
            raise Exception("Invalid node name [%s]"% name)
        return self._nodes_config[name]

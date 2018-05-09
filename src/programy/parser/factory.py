"""
Copyright (c) 2016-2018 Keith Sterling http://www.keithsterling.com

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

    @abstractmethod
    def default_config_file(self):
        raise NotImplementedError()

    def process_config_line(self, line):
        if self.valid_config_line(line):
            splits = line.split("=")
            node_name = splits[0].strip()
            if node_name in self._nodes_config:
                YLogger.error(self, "Node already exists in config [%s]", line)
                return
            class_name = splits[1].strip()
            YLogger.debug(self, "Pre-instantiating %s Node [%s]", self._type, class_name)
            try:
                self._nodes_config[node_name] = ClassLoader.instantiate_class(class_name)
            except Exception as e:
                YLogger.exception(self, "Failed pre-instantiating %s Node [%s]"%(self._type, class_name), e)

    def valid_config_line(self, line):

        if not line:
            return False

        if line.startswith('#'):
            return False

        if "=" not in line:
            YLogger.error(self, "Config line missing '=' [%s]", line)
            return False

        return True

    def load_nodes_config_from_file(self, filename=None):
        try:
            self._nodes_config.clear()

            if filename is None or os.path.exists(filename) is False:
                filename = self.default_config_file()

            with open(filename, "r", encoding="utf-8") as node_file:
                for line in node_file:
                    line = line.strip()
                    self.process_config_line(line)

        except Exception as excep:
            YLogger.exception(self, "Failed to load %s Node Factory config file [%s]"%(self._type, filename), excep)

    def load_nodes_config_from_text(self, text):
        self._nodes_config.clear()

        lines = text.split("\n")
        for line in lines:
            line = line.strip()
            self.process_config_line(line)

    def exists(self, node_name):
        return node_name in self._nodes_config

    def new_node_class(self, name):
        if name not in self._nodes_config:
            raise Exception("Invalid node name [%s]"% name)
        return self._nodes_config[name]

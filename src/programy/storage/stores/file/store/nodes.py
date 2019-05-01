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
import os.path

from programy.storage.stores.file.store.filestore import FileStore
from programy.storage.entities.nodes import NodesStore
from programy.utils.classes.loader import ClassLoader

class FileNodeStore(FileStore, NodesStore):

    def __init__(self, storage_engine):
        FileStore.__init__(self, storage_engine)

    def _load_file_contents(self, node_factory, filename):
        YLogger.debug(self, "Loading nodes from file [%s]", filename)
        count = 0
        try:
            with open(filename, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if line:
                        self.process_config_line(node_factory, line, filename)
        except FileNotFoundError:
            YLogger.error(self, "File not found [%s]", filename)

        return count

    def process_config_line(self, node_factory, line, filename):
        if self.valid_config_line(line, filename):
            splits = line.split("=")
            node_name = splits[0].strip()
            if node_name in node_factory.nodes:
                YLogger.error(self, "Node already exists in config [%s]", line)
                return
            class_name = splits[1].strip()
            YLogger.debug(self, "Pre-instantiating %s Node [%s]", node_factory.type, class_name)
            try:
                node_factory.add_node(node_name, ClassLoader.instantiate_class(class_name))
            except Exception as e:
                YLogger.exception_nostack(self, "Failed pre-instantiating %s Node [%s]"%(node_factory.type, class_name), e)

    def valid_config_line(self, line, filename):

        if not line:
            return False

        if line.startswith('#'):
            return False

        if "=" not in line:
            YLogger.error(self, "Config line missing '=' [%s] in [%s]", line, filename)
            return False

        return True


class FilePatternNodeStore(FileNodeStore):

    def __init__(self, storage_engine):
        FileNodeStore.__init__(self, storage_engine)

    def get_storage(self):
        return self.storage_engine.configuration.pattern_nodes_storage


class FileTemplateNodeStore(FileNodeStore):

    def __init__(self, storage_engine):
        FileNodeStore.__init__(self, storage_engine)

    def get_storage(self):
        return self.storage_engine.configuration.template_nodes_storage

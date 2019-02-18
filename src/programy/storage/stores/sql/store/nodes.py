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
import os
from programy.utils.logging.ylogger import YLogger
from programy.utils.classes.loader import ClassLoader

from programy.storage.stores.sql.store.sqlstore import SQLStore
from programy.storage.entities.nodes import NodesStore
from programy.storage.stores.sql.dao.node import PatternNode
from programy.storage.stores.sql.dao.node import TemplateNode
from programy.storage.entities.store import Store


class SQLNodesStore(SQLStore, NodesStore):

    def _get_storage_class(self):
        pass

    def load(self, node_factory):
        nodes = self.get_all_nodes()
        for node in nodes:
            try:
                node_factory.add_node(node.name, ClassLoader.instantiate_class(node.node_class))
            except Exception as e:
                YLogger.exception(self, "Failed pre-instantiating %s Node [%s]", e, node_factory.type, node.node_class)

    def upload_from_file(self, filename, format=Store.TEXT_FORMAT, commit=True, verbose=False):

        count = 0
        success = 0

        if os.path.exists(filename):

            try:
                with open(filename, "r", encoding="utf-8") as file:
                    for line in file:
                        if self._process_config_line(line, verbose) is True:
                            success += 1
                        count += 1

                if commit is True:
                    self.commit()

            except FileNotFoundError:
                YLogger.error(self, "File not found [%s]", filename)

        return count, success

    def _process_config_line(self, line, verbose=False):
        line = line.strip()
        if line:
            if line.startswith('#') is False:
                splits = line.split("=")
                node_name = splits[0].strip()
                class_name = splits[1].strip()
                node = self._get_entity(node_name, class_name)
                self.storage_engine.session.add(node)
                if verbose is True:
                    print("[%s] = [%s]"%(node_name, class_name))
                return True
        return False

    def _get_entity(self, name, classname):
        raise NotImplementedError()


class SQLPatternNodesStore(SQLNodesStore, NodesStore):

    def empty(self):
        self._storage_engine.session.query(PatternNode).delete()

    def get_all_nodes(self):
        return self._storage_engine.session.query(PatternNode)

    def _get_entity(self, name, classname):
        return PatternNode(name=name, node_class=classname)


class SQLTemplateNodesStore(SQLNodesStore, NodesStore):

    def empty(self):
        self._storage_engine.session.query(TemplateNode).delete()

    def get_all_nodes(self):
        return self._storage_engine.session.query(TemplateNode)

    def _get_entity(self, name, classname):
        return TemplateNode(name=name, node_class=classname)

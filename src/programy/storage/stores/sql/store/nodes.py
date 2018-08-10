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
from programy.utils.classes.loader import ClassLoader

from programy.storage.stores.sql.store.sqlstore import SQLStore
from programy.storage.entities.nodes import NodesStore
from programy.storage.stores.sql.dao.node import PatternNode
from programy.storage.stores.sql.dao.node import TemplateNode


class SQLNodesStore(SQLStore, NodesStore):

    def _get_storage_class(self):
        pass

    def load(self, node_factory):
        nodes = self.get_all_nodes()
        for node in nodes:
            try:
                node_factory.add_node(node.name, ClassLoader.instantiate_class(node.node_class))
            except Exception as e:
                YLogger.exception(self, "Failed pre-instantiating %s Node [%s]"%(node_factory.type, node.node_class), e)


class SQLPatternNodesStore(SQLNodesStore, NodesStore):

    def empty(self):
        self._storage_engine.session.query(PatternNode).delete()

    def get_all_nodes(self):
        return self._storage_engine.session.query(PatternNode)


class SQLTemplateNodesStore(SQLNodesStore, NodesStore):

    def empty(self):
        self._storage_engine.session.query(TemplateNode).delete()

    def get_all_nodes(self):
        return self._storage_engine.session.query(TemplateNode)


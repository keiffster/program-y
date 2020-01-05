"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

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
from programy.storage.stores.sql.store.sqlstore import SQLStore
from programy.storage.entities.maps import MapsReadWriteStore
from programy.storage.stores.sql.dao.map import Map


class SQLMapsStore(SQLStore, MapsReadWriteStore):

    def __init__(self, storage_engine):
        SQLStore.__init__(self, storage_engine)
        MapsReadWriteStore.__init__(self)

    def _get_all(self):
        return self._storage_engine.session.query(Map)

    def empty(self):
        self._get_all().delete()

    def empty_named(self, name):
        self._storage_engine.session.query(Map).filter(Map.name == name).delete()

    def _get_entity(self, name, key, value):
        return Map(name=name, key=key, value=value)

    def add_to_map(self, name, key, value, overwrite_existing=False):
        del overwrite_existing
        amap = self. _get_entity(name, key, value)
        self._storage_engine.session.add(amap)
        return True

    def remove_from_map(self, name, key):
        if self._storage_engine.session.query(Map).filter(Map.name == name, Map.key == key).delete() > 0:
            return True

        return False

    def load_all(self, collector):
        collector.empty()
        names = self._storage_engine.session.query(Map.name).distinct()
        for name in names:
            self.load(collector, name[0])
        return True

    def load(self, collector, name=None):
        collector.remove(name)
        values = self._storage_engine.session.query(Map).filter(Map.name == name)
        the_map = {}
        for item in values:
            the_map[item.key] = item.value

        if len(the_map):
            collector.add_map(name, the_map, 'sql')
            return True

        return False
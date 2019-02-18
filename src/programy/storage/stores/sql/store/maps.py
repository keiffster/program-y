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
from programy.storage.stores.sql.store.sqlstore import SQLStore
from programy.storage.entities.maps import MapsStore
from programy.storage.stores.sql.dao.map import Map


class SQLMapsStore(SQLStore, MapsStore):

    def empty(self):
        self._storage_engine.session.query(Map).delete()

    def empty_named(self, name):
        self._storage_engine.session.query(Map).filter(Map.name == name).delete()

    def _get_entity(self, name, key, value):
        return Map(name=name, key=key, value=value)

    def add_to_map(self, name, key, value, overwrite_existing=False):
        amap = Map(name=name, key=key, value=value)
        self._storage_engine.session.add(amap)
        return True

    def remove_from_map(self, name, key):
        self._storage_engine.session.query(Map).filter(Map.name==name, Map.key==key).delete()

    def load_all(self, map_collection):
        map_collection.empty()
        names = self._storage_engine.session.query(Map.name).distinct()
        for name in names:
            self.load(map_collection, name[0])

    def load(self, map_collection, map_name):
        map_collection.remove(map_name)
        values = self._storage_engine.session.query(Map).filter(Map.name==map_name)
        the_map = {}
        for item in values:
            the_map[item.key] = item.value
        map_collection.add_map(map_name, the_map, 'sql')

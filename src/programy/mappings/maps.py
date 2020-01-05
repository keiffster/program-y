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
from programy.utils.logging.ylogger import YLogger
from programy.storage.factory import StorageFactory


class MapCollection:

    def __init__(self, split_char=":", eol="\n"):
        self._split_char = split_char
        self._eol = eol
        self._maps = {}
        self._stores = {}

    @property
    def maps(self):
        return self._maps

    @property
    def stores(self):
        return self._stores

    def empty(self):
        self._maps.clear()
        self._stores.clear()

    def map(self, name):
        map_name = name.upper()
        return self._maps[map_name]

    def storename(self, mapname):
        if mapname in self._stores:
            return self._stores[mapname]
        return None
    
    def add_map(self, name, the_map, map_store):
        self._maps[name.upper()] = the_map
        self._stores[name.upper()] = map_store

    def remove(self, map_name):
        self._maps.pop(map_name, None)
        self._stores.pop(map_name, None)

    def contains(self, name):
        map_name = name.upper()
        return bool(map_name in self._maps)

    def _load_collection(self, maps_store_engine):
        maps_store = maps_store_engine.maps_store()
        maps_store.load_all(self)

    def load(self, storage_factory):
        if storage_factory.entity_storage_engine_available(StorageFactory.MAPS) is True:
            maps_store_engine = storage_factory.entity_storage_engine(StorageFactory.MAPS)
            try:
                self._load_collection(maps_store_engine)

            except Exception as e:
                YLogger.exception(self, "Failed to load map from storage", e)

        return len(self._maps)

    def _reload_collection(self, maps_store_engine, map_name):
        maps_store = maps_store_engine.maps_store()
        maps_store.reload(self, map_name)

    def reload(self, storage_factory, map_name):
        if storage_factory.entity_storage_engine_available(StorageFactory.MAPS) is True:
            maps_store_engine = storage_factory.entity_storage_engine(StorageFactory.MAPS)
            try:
                self._reload_collection(maps_store_engine, map_name)

            except Exception as e:
                YLogger.exception(self, "Failed to load map from storage", e)

        return len(self._maps)

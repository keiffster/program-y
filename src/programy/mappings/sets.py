"""
Copyright(c) 2016-2019 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files(the "Software"), to deal in the Software without restriction, including without limitation
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


class SetCollection(object):

    def __init__(self):
        self._sets = {}
        self._stores = {}

    @property
    def sets(self):
        return self._sets

    @property
    def stores(self):
        return self._stores

    def storename(self, mapname):
        if mapname in self._stores:
            return self._stores[mapname]
        return None

    def empty(self):
        self._sets.clear()
        self._stores.clear()

    def remove(self, set_name):
        self._sets.pop(set_name, None)
        self._stores.pop(set_name, None)

    def add_set(self, set_name, the_set, set_store):

        # Set names always stored in upper case to handle ambiquity
        set_name = set_name.upper()

        if set_name in self._sets:
            raise Exception("Set %s already exists" % set_name)

        YLogger.debug(self, "Adding set [%s][%s] to set group", set_name, set_store)
        self._sets[set_name] = the_set
        self._stores[set_name] = set_store

    def contains(self, name):
        # Set names always stored in upper case to handle ambiquity
        set_name = name.upper()
        return bool(set_name in self._sets)

    def set(self, name):
        # Set names always stored in upper case to handle ambiquity
        set_name = name.upper()
        if set_name in self._sets:
            return self._sets[set_name]
        return None

    def store_name(self, set_name):
        if set_name in self._stores:
            return self._stores[set_name]
        return None

    def count_words_in_sets(self):
        count = 0
        for name, aset in self._sets.items():
            for value in aset:
                for variant in value:
                    count += len(variant)
        return count

    def load(self, storage_factory):
        if storage_factory.entity_storage_engine_available(StorageFactory.SETS) is True:
            sets_store_engine = storage_factory.entity_storage_engine(StorageFactory.SETS)
            if sets_store_engine:
                try:
                    sets_store = sets_store_engine.sets_store()
                    sets_store.load_all(self)
                except Exception as e:
                    YLogger.exception(self, "Failed to load set from storage", e)

        return len(self._sets)

    def reload(self, storage_factory, set_name):
        if storage_factory.entity_storage_engine_available(StorageFactory.SETS) is True:
            set_engine = storage_factory.entity_storage_engine(StorageFactory.SETS)
            if set_engine:
                try:
                    sets_store = set_engine.sets_store()
                    sets_store.reload(self, set_name)
                except Exception as e:
                    YLogger.exception(self, "Failed to load set from storage", e)


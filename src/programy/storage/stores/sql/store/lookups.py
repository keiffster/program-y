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
from programy.storage.stores.sql.store.sqlstore import SQLStore
from programy.storage.entities.lookups import LookupsStore
from programy.storage.stores.sql.dao.lookup import Lookup


class SQLLookupsStore(SQLStore, LookupsStore):

    def empty(self):
        self._storage_engine.session.query(Lookup).delete()

    def empty_named(self, name):
        self._storage_engine.session.query(Lookup).filter(Lookup.name==name).delete()

    def add_to_lookup(self, name, key, value):
        lookup = Lookup(name=name, key=key, value=value)
        self._storage_engine.session.add(lookup)
        return lookup

    def remove_lookup(self, name):
        self._storage_engine.session.query(Lookup).filter(Lookup.name==name).delete()

    def remove_lookup_key(self, name, key):
        self._storage_engine.session.query(Lookup).filter(Lookup.name==name, Lookup.key==key).delete()

    def get_lookup(self, name):
        db_lookups = self._storage_engine.session.query(Lookup).filter(Lookup.name==name)
        lookups = []
        for lookup in db_lookups:
            lookups.append({"key": lookup.key, "value": lookup.value})
        if lookups:
            return lookups
        return None

    def load_all(self, lookup_collection):
        lookup_collection.empty()
        names = self._storage_engine.session.query(Lookup.name).distinct()
        for name in names:
            self.load(lookup_collection, name[0])

    def load(self, lookup_collection, name):
        lookup_collection.empty()
        values = self._storage_engine.session.query(Lookup).filter(Lookup.name==name)
        for pair in values:
            key = pair.key.strip('"')
            value = pair.value.strip('"')
            index, pattern = self.process_key_value(key, value)
            lookup_collection.add_to_lookup(index,  pattern)

    def process_line(self, name, fields):
        if fields:
            key = fields[0].upper()
            alookup = Lookup(name=name, key=key, value=fields[1])
            self._storage_engine.session.add(alookup)

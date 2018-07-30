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
from programy.storage.stores.nosql.mongo.store.mongostore import MongoStore
from programy.storage.entities.lookups import LookupsStore
from programy.storage.stores.nosql.mongo.dao.lookup import Lookup


class MongoLookupStore(MongoStore, LookupsStore):

    def __init__(self, storage_engine):
        MongoStore.__init__(self, storage_engine)

    def collection_name(self):
        return 'lookups'

    def empty_named(self, name):
        collection = self.collection()
        collection.remove({"name": name})

    def add_to_lookup(self, name, key, value):
        collection = self.collection()
        lookup = collection.find_one({"name": name})
        if lookup is not None:
            lookup['key_values'][key] = value
            collection.update({"name": name}, lookup)
        else:
            lookup = Lookup(name, {key: value})
            self.add_document(lookup)
        return lookup

    def remove_lookup(self, name):
        collection = self.collection()
        collection.delete_many({"name": name})

    def remove_lookup_key(self, name, key):
        collection = self.collection()
        lookup = collection.find_one({"name": name})
        if lookup is not None:
            if key in lookup['key_values']:
                lookup['key_values'].pop(key)
                collection.update({"name": name}, lookup)

    def get_lookup(self, name):
        collection = self.collection()
        lookup = collection.find_one({"name": name})
        if lookup is not None:
            return lookup['key_values']
        return None

    def load_all(self, lookup_collection):
        collection = self.collection()

        lookup_collection.empty()

        lookups = collection.find()
        for lookup in lookups:
            self._load_lookup(lookup_collection, lookup)

    def load(self, lookup_collection, name):
        collection = self.collection()

        lookup = collection.find_one({"name": name})

        self._load_lookup(lookup_collection, lookup)

    def _load_lookup(self, lookup_collection, lookup):
        for key, value in lookup['key_values'].items():
            key = key.strip('"')
            value =  value.strip('"')
            index, pattern = self.process_key_value(key, value)
            lookup_collection.add_to_lookup(index,  pattern)

    def process_line(self, name, fields):
        if fields:
            key = fields[0].upper()
            value = fields[1]
            self.add_to_lookup(name, key, value)

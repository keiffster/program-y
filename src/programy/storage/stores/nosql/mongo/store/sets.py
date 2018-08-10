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
from programy.storage.entities.sets import SetsStore
from programy.storage.stores.nosql.mongo.dao.set import Set

class MongoSetsStore(MongoStore, SetsStore):

    def __init__(self, storage_engine):
        MongoStore.__init__(self, storage_engine)

    def collection_name(self):
        return 'sets'

    def empty_named(self, name):
        collection = self.collection ()
        collection.remove({"name": name})

    def add_to_set(self, name, value):
        collection = self.collection()
        aset = collection.find_one({"name": name})
        if aset is not None:
            aset['values'].append(value.upper())
            collection.update({"name": name}, aset)
        else:
            aset = Set(name, [value.upper()])
            self.add_document(aset)
        return aset

    def remove_from_set(self, name, value):
        collection = self.collection()
        aset = collection.find_one({"name": name})
        if aset is not None:
            if value.upper() in aset['values']:
                aset['values'].remove(value.upper())
                if aset['values']:
                    collection.update({"name": name}, aset)
                else:
                    collection.remove({"name": name})

    def load_all(self, set_collection):
        collection = self.collection ()
        set_collection.empty()
        sets = collection.find({})
        for aset in sets:
            self.load(set_collection, aset['name'])

    def load(self, set_collection, set_name):
        collection = self.collection ()
        aset = collection.find_one({"name": set_name})
        if aset is not None:
            set_collection.remove(set_name)
            set_collection.add_set(set_name, aset['values'], 'mongo')

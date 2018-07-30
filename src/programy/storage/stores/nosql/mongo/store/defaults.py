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
from programy.storage.entities.defaults import DefaultStore
from programy.storage.stores.nosql.mongo.dao.default import Default


class MongoDefaultStore(MongoStore, DefaultStore):

    def __init__(self, storage_engine):
        MongoStore.__init__(self, storage_engine)

    def collection_name(self):
        return 'defaults'

    def empty_defaults(self):
        collection = self.collection()
        collection.remove()

    def add_default(self, name, value):
        collection = self.collection()
        default = collection.find_one({"name": name})
        if default is not None:
            default.value = value
            collection.update(default)
        else:
            default = Default()
            default.name = name
            default.value = value
            self.add_document(default)
        return default

    def add_defaults(self, defaults):
        for name, value in defaults.items():
            self.add_default(name, value)

    def get_default_values(self):
        collection = self.collection()
        props_colleciton = collection.find()
        defaults = {}
        if props_colleciton is not None:
            for default in props_colleciton:
                defaults[default['name']] = default['value']
        return defaults

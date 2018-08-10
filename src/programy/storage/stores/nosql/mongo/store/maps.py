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
from programy.storage.entities.maps import MapsStore
from programy.storage.stores.nosql.mongo.dao.map import Map

class MongoMapsStore(MongoStore, MapsStore):

    def __init__(self, storage_engine):
        MongoStore.__init__(self, storage_engine)

    def collection_name(self):
        return 'maps'

    def empty_named(self, name):
        collection = self.collection ()
        collection.remove({"name": name})

    def add_to_map(self, name, key, value):
        collection = self.collection()
        map = collection.find_one({"name": name})
        if map is not None:
            map['key_values'][key] = value
            collection.update({"name": name}, map)
        else:
            map = Map(name, {key: value})
            self.add_document(map)
        return map

    def remove_from_map(self, name, key):
        collection = self.collection()
        map = collection.find_one({"name": name})
        if map is not None:
            if key in map['key_values']:
                map['key_values'].pop(key)
                if map['key_values']:
                    collection.update({"name": name}, map)
                else:
                    collection.remove({"name": name})

    def load_all(self, map_collection):
        collection = self.collection ()
        map_collection.empty()
        maps = collection.find({})
        for map in maps:
            self.load(map_collection, map['name'])

    def load(self, map_collection, map_name):
        collection = self.collection ()
        map = collection.find_one({"name": map_name})
        if map is not None:
            map_collection.remove(map_name)
            map_collection.add_map(map_name, map['key_values'], 'mongo')

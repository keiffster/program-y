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
from programy.utils.logging.ylogger import YLogger
from programy.storage.stores.nosql.mongo.store.mongostore import MongoStore
from programy.storage.entities.maps import MapsStore
from programy.storage.stores.nosql.mongo.dao.map import Map

class MongoMapsStore(MongoStore, MapsStore):

    MAPS = 'maps'
    NAME = 'name'
    KEYVALUES = 'key_values'

    def __init__(self, storage_engine):
        MongoStore.__init__(self, storage_engine)

    def collection_name(self):
        return MongoMapsStore.MAPS

    def empty_named(self, name):
        YLogger.info(self, "Empting map in Mongo [%s]", name)
        collection = self.collection ()
        collection.remove({MongoMapsStore.NAME: name})

    def add_to_map(self, name, key, value, overwrite_existing=False):
        collection = self.collection()
        map = collection.find_one({MongoMapsStore.NAME: name})
        if map is not None:
            if key in map[MongoMapsStore.KEYVALUES]:
                if overwrite_existing is True:
                    YLogger.info(self, "Updating map in Mongo", name, key, value)
                    map[MongoMapsStore.KEYVALUES][key] = value
                    collection.replace_one({MongoMapsStore.NAME: name}, map)
                else:
                    YLogger.error(self, "Existing value in map [%s] [%s] = [%s] in Mongo", name, key, value)
                    return False
            else:
                map[MongoMapsStore.KEYVALUES][key] = value
                collection.replace_one({MongoMapsStore.NAME: name}, map)
        else:
            map = Map(name, {key: value})
            self.add_document(map)
        return True

    def remove_from_map(self, name, key):
        YLogger.info(self, "Removing key [%s] from map [%s] in Mongo", name, key)
        collection = self.collection()
        map = collection.find_one({MongoMapsStore.NAME: name})
        if map is not None:
            if key in map[MongoMapsStore.KEYVALUES]:
                map[MongoMapsStore.KEYVALUES].pop(key)
                if map[MongoMapsStore.KEYVALUES]:
                    collection.replace_one({MongoMapsStore.NAME: name}, map)
                else:
                    collection.delete_one({MongoMapsStore.NAME: name})

    def load_all(self, map_collection):
        YLogger.info(self, "Loading all maps from Mongo")
        collection = self.collection ()
        map_collection.empty()
        maps = collection.find({})
        for map in maps:
            self.load(map_collection, map[MongoMapsStore.NAME])

    def load(self, map_collection, map_name):
        YLogger.info(self, "Loading map [%s] from Mongo", map_name)
        collection = self.collection ()
        map = collection.find_one({MongoMapsStore.NAME: map_name})
        if map is not None:
            map_collection.remove(map_name)
            map_collection.add_map(map_name, map[MongoMapsStore.KEYVALUES], MongoStore.MONGO)

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
from programy.storage.stores.nosql.mongo.store.mongostore import MongoStore
from programy.storage.entities.maps import MapsReadWriteStore
from programy.storage.stores.nosql.mongo.dao.map import Map


class MongoMapsStore(MongoStore, MapsReadWriteStore):
    MAPS = 'maps'
    NAME = 'name'
    KEYVALUES = 'key_values'

    def __init__(self, storage_engine):
        MongoStore.__init__(self, storage_engine)
        MapsReadWriteStore.__init__(self)

    def collection_name(self):
        return MongoMapsStore.MAPS

    def empty_named(self, name):
        YLogger.info(self, "Empting map in Mongo [%s]", name)
        collection = self.collection()
        collection.remove({MongoMapsStore.NAME: name})

    def add_to_map(self, name, key, value, overwrite_existing=False):
        collection = self.collection()
        amap = collection.find_one({MongoMapsStore.NAME: name})
        if amap is not None:
            if key in amap[MongoMapsStore.KEYVALUES]:
                if overwrite_existing is True:
                    YLogger.info(self, "Updating map [%s] in Mongo [%s]=[%s]", name, key, value)
                    amap[MongoMapsStore.KEYVALUES][key] = value
                    result = collection.replace_one({MongoMapsStore.NAME: name}, amap)
                    return bool(result.modified_count > 0)
                else:
                    YLogger.error(self, "Existing value in map [%s] [%s] = [%s] in Mongo", name, key, value)
            else:
                amap[MongoMapsStore.KEYVALUES][key] = value
                result = collection.replace_one({MongoMapsStore.NAME: name}, amap)
                return bool(result.modified_count > 0)

        else:
            amap = Map(name, {key: value})
            return self.add_document(amap)

        return False

    def remove_from_map(self, name, key):
        YLogger.info(self, "Removing key [%s] from map [%s] in Mongo", name, key)
        collection = self.collection()
        amap = collection.find_one({MongoMapsStore.NAME: name})
        if amap is not None:
            amap[MongoMapsStore.KEYVALUES].pop(key)
            if amap[MongoMapsStore.KEYVALUES]:
                result = collection.replace_one({MongoMapsStore.NAME: name}, amap)
                return bool(result.modified_count > 0)

            else:
                result = collection.delete_one({MongoMapsStore.NAME: name})
                return bool(result.deleted_count > 0)

        return False

    def load_all(self, collector):
        YLogger.info(self, "Loading all maps from Mongo")
        collection = self.collection()
        collector.empty()
        maps = collection.find({})
        for amap in maps:
            self.load(collector, amap[MongoMapsStore.NAME])

    def load(self, collector, name=None):
        YLogger.info(self, "Loading map [%s] from Mongo", name)
        collection = self.collection()
        amap = collection.find_one({MongoMapsStore.NAME: name})
        if amap is not None:
            collector.remove(name)
            collector.add_map(name, amap[MongoMapsStore.KEYVALUES], MongoStore.MONGO)
            return True

        return False

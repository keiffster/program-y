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
from programy.storage.entities.sets import SetsReadWriteStore
from programy.storage.stores.nosql.mongo.dao.set import Set


class MongoSetsStore(MongoStore, SetsReadWriteStore):
    SETS = 'sets'
    NAME = 'name'
    VALUES = 'values'

    def __init__(self, storage_engine):
        MongoStore.__init__(self, storage_engine)
        SetsReadWriteStore.__init__(self)

    def collection_name(self):
        return MongoSetsStore.SETS

    def empty_named(self, name):
        YLogger.info(self, "Empting set [%s]", name)
        collection = self.collection()
        collection.remove({MongoSetsStore.NAME: name})

    def add_to_set(self, name, value, replace_existing=False):
        collection = self.collection()
        aset = collection.find_one({MongoSetsStore.NAME: name})
        uvalue = value.upper()
        if aset is not None:
            if uvalue not in aset[MongoSetsStore.VALUES]:
                YLogger.info(self, "Adding value to set [%s] [%s]", name, uvalue)
                aset[MongoSetsStore.VALUES].append(uvalue)
                result = collection.replace_one({MongoSetsStore.NAME: name}, aset)
                return bool(result.modified_count > 0)

        else:
            YLogger.info(self, "Creating new set [%s], initial value [%s]", name, uvalue)
            aset = Set(name, [uvalue])
            return self.add_document(aset)

    def remove_from_set(self, name, value):
        YLogger.info(self, "Remove value [%s] from set [%s]", value, name)
        collection = self.collection()
        aset = collection.find_one({MongoSetsStore.NAME: name})
        if aset is not None:
            if value.upper() in aset[MongoSetsStore.VALUES]:
                aset[MongoSetsStore.VALUES].remove(value.upper())
                if aset[MongoSetsStore.VALUES]:
                    result = collection.replace_one({MongoSetsStore.NAME: name}, aset)
                    return bool(result.modified_count > 0)

                else:
                    result = collection.delete_one({MongoSetsStore.NAME: name})
                    return bool(result.deleted_count > 0)

        return False


    def load_all(self, collector):
        YLogger.info(self, "Loading all sets from Mongo")
        collection = self.collection()
        collector.empty()
        sets = collection.find({})
        for aset in sets:
            self.load(collector, aset[MongoSetsStore.NAME])

    def load(self, collector, name=None):
        YLogger.info(self, "Loading set [%s] from Mongo", name)
        collection = self.collection()
        aset = collection.find_one({MongoSetsStore.NAME: name})
        if aset is not None:
            the_set = {}
            for value in aset[MongoSetsStore.VALUES]:
                value = value.strip()
                self.add_set_values(the_set, value)

            collector.remove(name)
            collector.add_set(name, the_set, MongoStore.MONGO)
            return True

        return False

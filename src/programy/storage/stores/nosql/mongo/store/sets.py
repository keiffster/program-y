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
from programy.storage.entities.sets import SetsStore
from programy.storage.stores.nosql.mongo.dao.set import Set

class MongoSetsStore(MongoStore, SetsStore):

    SETS = 'sets'
    NAME = 'name'
    VALUES = 'values'
    
    def __init__(self, storage_engine):
        MongoStore.__init__(self, storage_engine)

    def collection_name(self):
        return MongoSetsStore.SETS

    def empty_named(self, name):
        YLogger.info(self, "Empting set [%s]", name)
        collection = self.collection ()
        collection.remove({MongoSetsStore.NAME: name})

    def add_to_set(self, name, value, replace_existing=False):
        collection = self.collection()
        aset = collection.find_one({MongoSetsStore.NAME: name})
        uvalue = value.upper()
        if aset is not None:
            if uvalue not in aset[MongoSetsStore.VALUES]:
                YLogger.info(self, "Adding value to set [%s] [%s]", name, uvalue)
                aset[MongoSetsStore.VALUES].append(uvalue)
                collection.replace_one({MongoSetsStore.NAME: name}, aset)
                return True
            else:
                if replace_existing is True:
                    YLogger.info(self, "Updating set [%s] [%s]", name, uvalue)
                    aset[MongoSetsStore.VALUES] = uvalue
                    collection.replace_one({MongoSetsStore.NAME: name}, aset)
                    return True
                else:
                    YLogger.error(self, "Existing value in set [%s] [%s]", name, uvalue)
                    return False
        else:
            YLogger.info(self, "Creating new set [%s], initial value [%s]", name, uvalue)
            aset = Set(name, [uvalue])
            self.add_document(aset)
            return True

    def remove_from_set(self, name, value):
        YLogger.info(self, "Remove value [%s] from set [%s]", value, name)
        collection = self.collection()
        aset = collection.find_one({MongoSetsStore.NAME: name})
        if aset is not None:
            if value.upper() in aset[MongoSetsStore.VALUES]:
                aset[MongoSetsStore.VALUES].remove(value.upper())
                if aset[MongoSetsStore.VALUES]:
                    collection.replace_one({MongoSetsStore.NAME: name}, aset)
                else:
                    collection.delete_one({MongoSetsStore.NAME: name})

    def load_all(self, set_collection):
        YLogger.info(self, "Loading all sets from Mongo")
        collection = self.collection ()
        set_collection.empty()
        sets = collection.find({})
        for aset in sets:
            self.load(set_collection, aset[MongoSetsStore.NAME])

    def load(self, set_collection, set_name):
        YLogger.info(self, "Loading set [%s] from Mongo", set_name)
        collection = self.collection ()
        aset = collection.find_one({MongoSetsStore.NAME: set_name})
        if aset is not None:
            the_set = {}
            for value in  aset[MongoSetsStore.VALUES]:
                value = value.strip()
                if value:
                    self.add_set_values(the_set, value)

            set_collection.remove(set_name)
            set_collection.add_set(set_name, the_set, MongoStore.MONGO)

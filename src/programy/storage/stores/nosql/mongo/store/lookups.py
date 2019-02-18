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
from programy.storage.entities.lookups import LookupsStore
from programy.storage.stores.nosql.mongo.dao.lookup import Lookup
from programy.mappings.base import DoubleStringPatternSplitCollection


class MongoLookupStore(MongoStore, LookupsStore):

    def __init__(self, storage_engine):
        MongoStore.__init__(self, storage_engine)

    def collection_name(self):
        raise NotImplementedError()

    def add_to_lookup(self, key, value, overwrite_existing=False):
        collection = self.collection()
        lookup = collection.find_one({'key': key})
        if lookup is not None:
            if overwrite_existing is True:
                YLogger.info(self, "Updating lookup in Mongo [%s] [%s]", key, value)
                lookup['value'] = value
                collection.replace_one({'key': key}, lookup)
            else:
                YLogger.error(self, "Existing value in Mongo lookup [%s] = [%s]", key, value)
                return False
        else:
            YLogger.debug(self, "Adding lookup to Mongo [%s] = [%s]", key, value)
            lookup = Lookup(key, value)
            self.add_document(lookup)
        return True

    def remove_lookup(self):
        YLogger.debug(self, "Removing lookup from Mongo [%s]", self.collection_name())
        collection = self.collection()
        collection.delete_many({})

    def remove_lookup_key(self, key):
        YLogger.debug(self, "Removing lookup key [%s] from [%s] in Mongo", key, self.collection_name())
        collection = self.collection()
        collection.delete_one({'key': key})

    def get_lookup(self):
        collection = self.collection()
        lookups = collection.find()
        if lookups is not None:
            collection = {}
            for lookup in lookups:
                collection[lookup['key']] = lookup['value']
            return collection
        return {}

    def load_all(self, lookup_collection):
        self.load(lookup_collection)

    def load(self, lookup_collection):
        YLogger.debug(self, "Loading lookup from Mongo [%s]", self.collection_name())
        collection = self.collection()
        lookups = collection.find()
        if lookups is not None:
            for lookup in lookups:
                key, value = DoubleStringPatternSplitCollection.process_key_value(lookup['key'], lookup['value'])
                lookup_collection.add_to_lookup(key, value)

    def process_line(self, name, fields):
        if fields:
            key = fields[0].upper()
            value = fields[1]
            return self.add_to_lookup(key, value)
        return False


class MongoDenormalStore(MongoLookupStore):

    def __init__(self, storage_engine):
        MongoStore.__init__(self, storage_engine)

    def collection_name(self):
        return "denormals"


class MongoNormalStore(MongoLookupStore):

    def __init__(self, storage_engine):
        MongoStore.__init__(self, storage_engine)

    def collection_name(self):
        return "normals"


class MongoGenderStore(MongoLookupStore):

    def __init__(self, storage_engine):
        MongoStore.__init__(self, storage_engine)

    def collection_name(self):
        return "genders"


class MongoPersonStore(MongoLookupStore):

    def __init__(self, storage_engine):
        MongoStore.__init__(self, storage_engine)

    def collection_name(self):
        return "persons"


class MongoPerson2Store(MongoLookupStore):

    def __init__(self, storage_engine):
        MongoStore.__init__(self, storage_engine)

    def collection_name(self):
        return "person2s"

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
from programy.storage.entities.store import Store


class MongoStore(Store):
    MONGO = "mongo"

    def __init__(self, storage_engine):
        Store.__init__(self)
        self._storage_engine = storage_engine

    @property
    def storage_engine(self):
        return self._storage_engine

    def drop(self):
        YLogger.info(self, "Dropping mongo storage")
        self.collection().drop()

    def commit(self, commit=True):
        del commit
        YLogger.info(self, "Commit collection not supported on Mongo")

    def rollback(self, commit=True):
        del commit
        YLogger.info(self, "Rollback collection not supported on Mongo")

    def collection_name(self):
        raise NotImplementedError()  # pragma: no cover

    def collection(self):
        return self._storage_engine.database[self.collection_name()]

    def empty(self):
        YLogger.info(self, "Emptying collection [%s]", self.collection_name())
        collection = self.collection()
        collection.delete_many({})

    def _add_to_collection(self, collection, document):
        result = collection.insert_one(document.to_document())
        return result.inserted_id

    def add_document(self, document):
        YLogger.debug(self, "Adding document to collection [%s]", self.collection_name())
        collection = self.collection()
        document.id = self._add_to_collection(collection, document)
        return bool(document.id is not None)

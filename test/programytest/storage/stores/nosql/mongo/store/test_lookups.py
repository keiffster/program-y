from programytest.storage.asserts.store.assert_lookups import LookupStoreAsserts
import os
import os.path

from programy.storage.stores.nosql.mongo.store.lookups import MongoLookupStore
from programy.storage.stores.nosql.mongo.engine import MongoStorageEngine
from programy.storage.stores.nosql.mongo.config import MongoStorageConfiguration

class MongoLookupStoreTests(LookupStoreAsserts):

    def test_initialise(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoLookupStore(engine)
        self.assertEquals(store.storage_engine, engine)

    def test_lookup_storage(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoLookupStore(engine)

        self.assert_lookup_storage(store)

    def test_upload_from_text(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoLookupStore(engine)

        self.assert_upload_from_text(store)

    def test_upload_from_text_file(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoLookupStore(engine)

        self.assert_upload_from_text_file(store,os.path.dirname(__file__)+os.sep+"data"+os.sep+"lookups"+os.sep+"text"+os.sep+"gender.txt")

    def test_upload_csv_file(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoLookupStore(engine)

        self.assert_upload_csv_file(store, os.path.dirname(__file__)+os.sep+"data"+os.sep+"lookups"+os.sep+"csv"+os.sep+"gender.csv")

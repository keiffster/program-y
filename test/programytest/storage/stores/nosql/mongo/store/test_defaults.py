from programytest.storage.asserts.store.assert_defaults import DefaultStoreAsserts

from programy.storage.stores.nosql.mongo.store.defaults import MongoDefaultStore
from programy.storage.stores.nosql.mongo.engine import MongoStorageEngine
from programy.storage.stores.nosql.mongo.config import MongoStorageConfiguration


class MongoDefaultStoreTests(DefaultStoreAsserts):

    def test_initialise(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoDefaultStore(engine)
        self.assertEquals(store.storage_engine, engine)

    def test_defaults_storage(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoDefaultStore(engine)

        self.assert_defaults_storage(store)

    def test_property_storage(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoDefaultStore(engine)

        self.assert_empty_defaults(store)

    def test_empty_defaults(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoDefaultStore(engine)

        self.assert_empty_defaults(store)

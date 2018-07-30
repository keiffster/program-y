from programytest.storage.asserts.store.assert_properties import PropertyStoreAsserts

from programy.storage.stores.nosql.mongo.store.properties import MongoPropertyStore
from programy.storage.stores.nosql.mongo.engine import MongoStorageEngine
from programy.storage.stores.nosql.mongo.config import MongoStorageConfiguration


class MongoPropertyStoreTests(PropertyStoreAsserts):

    def test_initialise(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoPropertyStore(engine)
        self.assertEquals(store.storage_engine, engine)

    def test_properties_storage(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoPropertyStore(engine)

        self.assert_properties_storage(store)

    def test_property_storage(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoPropertyStore(engine)

        self.assert_property_storage(store)

    def test_empty_properties(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoPropertyStore(engine)

        self.assert_empty_properties(store)

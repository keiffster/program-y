from programytest.storage.asserts.store.assert_category import CategoryStoreAsserts

from programy.storage.stores.nosql.mongo.store.categories import MongoCategoryStore
from programy.storage.stores.nosql.mongo.engine import MongoStorageEngine
from programy.storage.stores.nosql.mongo.config import MongoStorageConfiguration


class MongoCategoryStoreTests(CategoryStoreAsserts):

    def test_initialise(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoCategoryStore(engine)
        self.assertEquals(store.storage_engine, engine)

    def test_category_storage(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoCategoryStore(engine)
        self.assertEquals(store.storage_engine, engine)

        self.assert_category_storage(store)

    def test_category_by_groupid_storage(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoCategoryStore(engine)
        self.assertEquals(store.storage_engine, engine)

        self.assert_category_by_groupid_storage(store)


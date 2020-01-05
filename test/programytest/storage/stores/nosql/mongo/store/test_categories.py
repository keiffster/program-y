import unittest
import programytest.storage.engines as Engines
from programy.storage.stores.nosql.mongo.config import MongoStorageConfiguration
from programy.storage.stores.nosql.mongo.engine import MongoStorageEngine
from programy.storage.stores.nosql.mongo.store.categories import MongoCategoryStore
from programytest.storage.asserts.store.assert_category import CategoryStoreAsserts


class MongoCategoryStoreTests(CategoryStoreAsserts):

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_initialise(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoCategoryStore(engine)
        self.assertEqual(store.storage_engine, engine)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_category_storage(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoCategoryStore(engine)
        self.assertEqual(store.storage_engine, engine)

        self.assert_category_storage(store)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_category_by_groupid_storage(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoCategoryStore(engine)
        self.assertEqual(store.storage_engine, engine)

        self.assert_category_by_groupid_storage(store)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_upload_from_file(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoCategoryStore(engine)
        self.assertEqual(store.storage_engine, engine)

        self.assert_upload_from_file(store)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_upload_from_directory(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoCategoryStore(engine)
        self.assertEqual(store.storage_engine, engine)

        self.assert_upload_from_directory(store)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_empty_named(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoCategoryStore(engine)
        self.assertEqual(store.storage_engine, engine)

        self.assert_empty_name(store)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_load(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoCategoryStore(engine)
        self.assertEqual(store.storage_engine, engine)

        self.assert_load(store)

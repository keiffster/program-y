import unittest
import re
import programytest.storage.engines as Engines
from programy.storage.stores.nosql.mongo.config import MongoStorageConfiguration
from programy.storage.stores.nosql.mongo.engine import MongoStorageEngine
from programy.storage.stores.nosql.mongo.store.lookups import MongoLookupStore
from programy.mappings.base import DoubleStringPatternSplitCollection


class TestMongoLookupStore(MongoLookupStore):

    def __init__(self, storage_engine):
        MongoLookupStore.__init__(self, storage_engine)

    def collection_name(self):
        return "test"


class TestCollection(DoubleStringPatternSplitCollection):

    def __init__(self):
        DoubleStringPatternSplitCollection.__init__(self)


class MongoLookupStoreTests(unittest.TestCase):

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_initialise(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoLookupStore(engine)
        self.assertEqual(store.storage_engine, engine)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_add_to_lookup_overwrite_false(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = TestMongoLookupStore(engine)

        store.add_to_lookup("key1", "value1", overwrite_existing=False)
        store.add_to_lookup("key1", "value2", overwrite_existing=False)

        collection = TestCollection()

        store.load(collection)

        self.assertEquals(1, len(collection.pairs.keys()))
        self.assertTrue(collection.has_key("key1"))
        self.assertEqual([re.compile('(^key1|key1|key1$)', re.IGNORECASE), 'VALUE1'], collection.value("key1"))

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_add_to_lookup_overwrite_true(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = TestMongoLookupStore(engine)

        store.add_to_lookup("key1", "value1", overwrite_existing=True)
        store.add_to_lookup("key1", "value2", overwrite_existing=True)

        collection = TestCollection()

        store.load(collection)

        self.assertEquals(1, len(collection.pairs.keys()))
        self.assertTrue(collection.has_key("key1"))
        self.assertEqual([re.compile('(^key1|key1|key1$)', re.IGNORECASE), 'VALUE2'], collection.value("key1"))

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_load_no_collection(self):
        config = MongoStorageConfiguration()
        config.drop_all_first = True

        engine = MongoStorageEngine(config)
        engine.initialise()
        store = TestMongoLookupStore(engine)

        collection = TestCollection()

        store.load(collection)

        self.assertEquals(0, len(collection.pairs.keys()))

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_load_all(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = TestMongoLookupStore(engine)

        store.add_to_lookup("key1", "value1", overwrite_existing=True)

        collection = TestCollection()

        store.load_all(collection)

        self.assertEquals(1, len(collection.pairs.keys()))
        self.assertTrue(collection.has_key("key1"))
        self.assertEqual([re.compile('(^key1|key1|key1$)', re.IGNORECASE), 'VALUE1'], collection.value("key1"))

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_get_lookup_present(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = TestMongoLookupStore(engine)
        store.drop()

        store.add_to_lookup("key1", "value1", overwrite_existing=True)

        collection = store.get_lookup()
        self.assertIsNotNone(collection )

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_get_lookup_not_present(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = TestMongoLookupStore(engine)
        store.drop()

        collection = store.get_lookup()
        self.assertEquals({}, collection)
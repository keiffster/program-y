import unittest

import programytest.storage.engines as Engines
from programy.storage.stores.nosql.mongo.config import MongoStorageConfiguration
from programy.storage.stores.nosql.mongo.engine import MongoStorageEngine
from programy.storage.stores.nosql.mongo.store.maps import MongoMapsStore
from programytest.storage.asserts.store.assert_maps import MapStoreAsserts
from programy.mappings.maps import MapCollection


class MongoMapsStoreTests(MapStoreAsserts):

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_initialise(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoMapsStore(engine)
        self.assertEqual(store.storage_engine, engine)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_map_storage(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoMapsStore(engine)

        self.assert_map_storage(store)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_upload_from_text(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoMapsStore(engine)

        self.assert_upload_from_text(store)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_upload_text_files_from_directory_no_subdir(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoMapsStore(engine)

        self.assert_upload_text_files_from_directory_no_subdir(store)

    @unittest.skip("CSV not supported yet")
    def test_upload_from_csv_file(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoMapsStore(engine)

        self.assert_upload_from_csv_file(store)

    @unittest.skip("CSV not supported yet")
    def test_upload_csv_files_from_directory_with_subdir(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoMapsStore(engine)

        self.assert_upload_csv_files_from_directory_with_subdir(store)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_empty_named(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoMapsStore(engine)

        self.assert_empty_named(store)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_add_to_map_overwrite_existing(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoMapsStore(engine)

        store.add_to_map("TESTMAP", "key1", "value1", overwrite_existing=True)
        store.add_to_map("TESTMAP", "key2", "value2", overwrite_existing=True)
        store.add_to_map("TESTMAP", "key2", "value3", overwrite_existing=True)

        map_collection = MapCollection()
        store.load(map_collection, 'TESTMAP')

        self.assertEqual(1, len(map_collection.maps.keys()))
        self.assertTrue("TESTMAP" in map_collection.maps)
        self.assertTrue("val1", map_collection.maps['TESTMAP']['key1'])
        self.assertTrue("val3", map_collection.maps['TESTMAP']['key2'])

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_add_to_map_no_overwrite_existing(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoMapsStore(engine)

        store.add_to_map("TESTMAP", "key1", "value1", overwrite_existing=False)
        store.add_to_map("TESTMAP", "key2", "value2", overwrite_existing=False)
        store.add_to_map("TESTMAP", "key2", "value3", overwrite_existing=False)

        map_collection = MapCollection()
        store.load(map_collection, 'TESTMAP')

        self.assertEqual(1, len(map_collection.maps.keys()))
        self.assertTrue("TESTMAP" in map_collection.maps)
        self.assertTrue("val1", map_collection.maps['TESTMAP']['key1'])
        self.assertTrue("val2", map_collection.maps['TESTMAP']['key2'])

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_load_no_map_found(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoMapsStore(engine)

        store.add_to_map("TESTMAP", "key1", "value1", overwrite_existing=False)
        store.add_to_map("TESTMAP", "key2", "value2", overwrite_existing=False)
        store.add_to_map("TESTMAP", "key2", "value3", overwrite_existing=False)

        map_collection = MapCollection()
        self.assertTrue(store.load(map_collection, 'TESTMAP'))

        map_collection2 = MapCollection()
        self.assertFalse(store.load(map_collection2, 'TESTMAP2'))


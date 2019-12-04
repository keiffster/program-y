import unittest
from unittest.mock import patch
import programytest.storage.engines as Engines
from programy.storage.stores.nosql.mongo.config import MongoStorageConfiguration
from programy.storage.stores.nosql.mongo.engine import MongoStorageEngine
from programy.storage.stores.nosql.mongo.store.properties import MongoPropertyStore
from programytest.storage.asserts.store.assert_properties import PropertyStoreAsserts


class MongoPropertyStoreTests(PropertyStoreAsserts):

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_initialise(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoPropertyStore(engine)
        self.assertEqual(store.storage_engine, engine)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_split_into_fields(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoPropertyStore(engine)

        self.assertEquals(None, store.split_into_fields(""))
        self.assertEquals(None, store.split_into_fields("X"))
        self.assertEquals(['X', 'Y'], store.split_into_fields('"X","Y"'))
        self.assertEquals(['X', 'Y'], store.split_into_fields('"X","Y","Z"'))

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_properties_storage(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoPropertyStore(engine)

        self.assert_properties_storage(store)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_property_storage(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoPropertyStore(engine)

        self.assert_property_storage(store)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_duplicate_properties_storage(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoPropertyStore(engine)

        self.assert_duplicate_property_storage(store)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_empty_properties(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoPropertyStore(engine)

        self.assert_empty_properties(store)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_upload_from_file(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoPropertyStore(engine)

        self.assert_upload_from_file(store)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_upload_from_file_verbose(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoPropertyStore(engine)

        self.assert_upload_from_file_verbose(store)

    def patch_read_lines_from_file(self, filename, verbose):
        raise Exception("Mock Exception")

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    @patch("programy.storage.stores.nosql.mongo.store.properties.MongoPropertyStore._read_lines_from_file", patch_read_lines_from_file)
    def test_upload_from_file_with_exception(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoPropertyStore(engine)

        self.assert_upload_from_file_exception(store)

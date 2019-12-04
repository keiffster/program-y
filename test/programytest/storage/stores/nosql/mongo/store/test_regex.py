import unittest
from unittest.mock import patch
import programytest.storage.engines as Engines
from programy.storage.stores.nosql.mongo.config import MongoStorageConfiguration
from programy.storage.stores.nosql.mongo.engine import MongoStorageEngine
from programy.storage.stores.nosql.mongo.store.properties import MongoRegexesStore
from programytest.storage.asserts.store.assert_regex import RegexStoreAsserts


class MongoRegexesStoreTests(RegexStoreAsserts):

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_initialise(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoRegexesStore(engine)
        self.assertEqual(store.storage_engine, engine)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_defaults_storage(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoRegexesStore(engine)

        self.assert_regexes_storage(store)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_regex_storage(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoRegexesStore(engine)

        self.assert_regex_storage(store)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_empty_regexes(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoRegexesStore(engine)

        self.assert_empty_regexes(store)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_upload_from_file(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoRegexesStore(engine)

        self.assert_upload_from_file(store)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_add_to_collection(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoRegexesStore(engine)

        self.assert_add_to_collection(store)

    def patch_add_regex(self, name, value):
        raise Exception("Mock Exception")

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    @patch("programy.mappings.properties.RegexTemplatesCollection.add_regex", patch_add_regex)
    def test_add_to_collection_exception(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoRegexesStore(engine)

        self.assert_add_to_collection_collection(store)

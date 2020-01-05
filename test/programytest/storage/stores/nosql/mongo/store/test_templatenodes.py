import unittest
from unittest.mock import patch
import programytest.storage.engines as Engines
from programy.storage.stores.nosql.mongo.config import MongoStorageConfiguration
from programy.storage.stores.nosql.mongo.engine import MongoStorageEngine
from programy.storage.stores.nosql.mongo.store.nodes import MongoTemplateNodeStore
from programytest.storage.asserts.store.assert_templatenodes import TemplateNodesStoreAsserts


class MongoNodeStoreTests(TemplateNodesStoreAsserts):

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_initialise(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoTemplateNodeStore(engine)
        self.assertEqual(store.storage_engine, engine)
        
    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_load_nodes(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoTemplateNodeStore(engine)

        self.assert_load(store)

    @staticmethod
    def patch_instantiate_class(class_string):
        raise Exception("Mock Exception")

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    @patch("programy.utils.classes.loader.ClassLoader.instantiate_class", patch_instantiate_class)
    def test_load_nodes_exception(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoTemplateNodeStore(engine)

        self.assert_load_exception(store)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_upload_from_file(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoTemplateNodeStore(engine)

        self.assert_upload_from_file(store, verbose=False)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_upload_from_file_verbose(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoTemplateNodeStore(engine)

        self.assert_upload_from_file(store, verbose=True)

    def patch_load_nodes_from_file(self, filename, verbose):
        raise Exception("Mock Exception")

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    @patch("programy.storage.stores.nosql.mongo.store.nodes.MongoNodeStore._load_nodes_from_file", patch_load_nodes_from_file)
    def test_upload_from_file_exception(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoTemplateNodeStore(engine)

        self.assert_upload_from_file_exception(store)


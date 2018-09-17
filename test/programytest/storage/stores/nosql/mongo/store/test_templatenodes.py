import unittest

from programytest.storage.asserts.store.assert_templatenodes import TemplateNodesStoreAsserts

from programy.storage.stores.nosql.mongo.store.nodes import MongoTemplateNodeStore
from programy.storage.stores.nosql.mongo.engine import MongoStorageEngine
from programy.storage.stores.nosql.mongo.config import MongoStorageConfiguration

import programytest.storage.engines as Engines


class MongoNodeStoreTests(TemplateNodesStoreAsserts):

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_initialise(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoTemplateNodeStore(engine)
        self.assertEqual(store.storage_engine, engine)
        
    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_load_variables(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoTemplateNodeStore(engine)

        self.assert_upload_from_file(store)

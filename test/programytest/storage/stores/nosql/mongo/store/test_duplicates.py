import unittest

from programytest.storage.asserts.store.assert_duplicates import DuplicateStoreAsserts

from programy.storage.stores.nosql.mongo.store.duplicates import MongoDuplicatesStore
from programy.storage.stores.nosql.mongo.engine import MongoStorageEngine
from programy.storage.stores.nosql.mongo.config import MongoStorageConfiguration

import programytest.storage.engines as Engines


class MongoDuplicatesStoreTests(DuplicateStoreAsserts):

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_initialise(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoDuplicatesStore(engine)
        self.assertEqual(store.storage_engine, engine)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_save_duplicates(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoDuplicatesStore(engine)

        self.assert_duplicates(store)

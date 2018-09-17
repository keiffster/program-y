import unittest

from programytest.storage.asserts.store.assert_spelling import SpellingStoreAsserts

from programy.storage.stores.nosql.mongo.store.spelling import MongoSpellingStore
from programy.storage.stores.nosql.mongo.engine import MongoStorageEngine
from programy.storage.stores.nosql.mongo.config import MongoStorageConfiguration

import programytest.storage.engines as Engines


class MongoSpellingStoreTests(SpellingStoreAsserts):

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_initialise(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoSpellingStore(engine)
        self.assertEqual(store.storage_engine, engine)
        
    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_upload_from_file(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoSpellingStore(engine)

        self.assert_upload_from_file(store)

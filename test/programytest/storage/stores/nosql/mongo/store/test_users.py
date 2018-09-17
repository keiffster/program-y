import unittest

from programytest.storage.asserts.store.assert_users import UserStoreAsserts

from programy.storage.stores.nosql.mongo.store.users import MongoUserStore
from programy.storage.stores.nosql.mongo.engine import MongoStorageEngine
from programy.storage.stores.nosql.mongo.config import MongoStorageConfiguration

import programytest.storage.engines as Engines


class MongoUserStoreTests(UserStoreAsserts):

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_initialise(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoUserStore(engine)
        self.assertEqual(store.storage_engine, engine)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_user_storage(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoUserStore(engine)

        self.assert_user_storage(store)

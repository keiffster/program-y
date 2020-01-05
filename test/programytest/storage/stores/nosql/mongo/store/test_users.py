import unittest
from unittest.mock import patch
import programytest.storage.engines as Engines
from programy.storage.stores.nosql.mongo.config import MongoStorageConfiguration
from programy.storage.stores.nosql.mongo.engine import MongoStorageEngine
from programy.storage.stores.nosql.mongo.store.users import MongoUserStore
from programytest.storage.asserts.store.assert_users import UserStoreAsserts


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

    def patch_remove_user_from_db(self, userid, clientid):
        raise Exception("Mock Exception")

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    @patch("programy.storage.stores.nosql.mongo.store.users.MongoUserStore._remove_user_from_db", patch_remove_user_from_db)
    def test_remove_user_exception(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoUserStore(engine)

        self.assert_remove_user_exception(store)

    def patch_remove_user_from_all_clients_from_db(self, userid):
        raise Exception("Mock Exception")

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    @patch("programy.storage.stores.nosql.mongo.store.users.MongoUserStore._remove_user_from_all_clients_from_db", patch_remove_user_from_all_clients_from_db)
    def test_remove_user_from_all_clients_exception(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoUserStore(engine)

        self.assert_remove_user_from_all_clients_exception(store)

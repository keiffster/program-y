import unittest
from unittest.mock import patch
import programytest.storage.engines as Engines
from programy.storage.stores.sql.config import SQLStorageConfiguration
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.store.users import SQLUserStore
from programytest.storage.asserts.store.assert_users import UserStoreAsserts


class SQLUserStoreTests(UserStoreAsserts):

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_initialise(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLUserStore(engine)
        self.assertEqual(store.storage_engine, engine)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_user_storage(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLUserStore(engine)

        self.assert_user_storage(store)

    def patch_remove_user_from_db(self, userid, clientid):
        raise Exception("Mock Exception")

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    @patch("programy.storage.stores.sql.store.users.SQLUserStore._remove_user_from_db", patch_remove_user_from_db)
    def test_remove_user_exception(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLUserStore(engine)

        self.assert_remove_user_exception(store)

    def patch_remove_user_from_all_clients_from_db(self, userid):
        raise Exception("Mock Exception")

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    @patch("programy.storage.stores.sql.store.users.SQLUserStore._remove_user_from_all_clients_from_db", patch_remove_user_from_all_clients_from_db)
    def test_remove_user_from_all_clients_exception(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLUserStore(engine)

        self.assert_remove_user_from_all_clients_exception(store)

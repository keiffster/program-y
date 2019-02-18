import unittest

from programytest.storage.asserts.store.assert_linkedaccount import LinkedAccountStoreAsserts

from programy.storage.stores.sql.store.linkedaccounts import SQLLinkedAccountStore
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.config import SQLStorageConfiguration

import programytest.storage.engines as Engines


class SQLLinkedAccountStoreTests(LinkedAccountStoreAsserts):

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_initialise(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLLinkedAccountStore(engine)
        self.assertEqual(store.storage_engine, engine)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_linkedaccounts_storage(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLLinkedAccountStore(engine)

        self.assert_linkedaccounts_storage(store)

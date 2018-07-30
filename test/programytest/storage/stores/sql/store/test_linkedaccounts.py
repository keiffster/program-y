from programytest.storage.asserts.store.assert_linkedaccount import LinkedAccountStoreAsserts

from programy.storage.stores.sql.store.linkedaccounts import SQLLinkedAccountStore
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.config import SQLStorageConfiguration


class SQLLinkedAccountStoreTests(LinkedAccountStoreAsserts):

    def test_initialise(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLLinkedAccountStore(engine)
        self.assertEquals(store.storage_engine, engine)

    def test_linkedaccounts_storage(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLLinkedAccountStore(engine)

        self.assert_linkedaccounts_storage(store)

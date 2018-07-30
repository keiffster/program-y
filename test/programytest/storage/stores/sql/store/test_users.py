from programytest.storage.asserts.store.assert_users import UserStoreAsserts

from programy.storage.stores.sql.store.users import SQLUserStore
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.config import SQLStorageConfiguration


class SQLUserStoreTests(UserStoreAsserts):

    def test_initialise(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLUserStore(engine)
        self.assertEquals(store.storage_engine, engine)

    def test_user_storage(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLUserStore(engine)

        self.assert_user_storage(store)

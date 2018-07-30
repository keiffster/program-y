from programytest.storage.asserts.store.assert_category import CategoryStoreAsserts

from programy.storage.stores.sql.store.categories import SQLCategoryStore
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.config import SQLStorageConfiguration


class SQLCategoryStoreTests(CategoryStoreAsserts):

    def test_initialise(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLCategoryStore(engine)
        self.assertEquals(store.storage_engine, engine)

    def test_category_storage(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLCategoryStore(engine)
        self.assertEquals(store.storage_engine, engine)

        self.assert_category_storage(store)

    def test_category_by_groupid_storage(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLCategoryStore(engine)
        self.assertEquals(store.storage_engine, engine)

        self.assert_category_by_groupid_storage(store)


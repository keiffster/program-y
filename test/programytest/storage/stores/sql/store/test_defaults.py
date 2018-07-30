from programytest.storage.asserts.store.assert_defaults import DefaultStoreAsserts

from programy.storage.stores.sql.store.defaults import SQLDefaultsStore
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.config import SQLStorageConfiguration


class SQLDefaultsStoreTests(DefaultStoreAsserts):

    def test_initialise(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLDefaultsStore(engine)
        self.assertEquals(store.storage_engine, engine)

    def test_defaults_storage(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLDefaultsStore(engine)

        self.assert_defaults_storage(store)

    def test_property_storage(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLDefaultsStore(engine)

        self.assert_defaults_storage(store)

    def test_empty_defaults(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLDefaultsStore(engine)

        self.assert_empty_defaults(store)


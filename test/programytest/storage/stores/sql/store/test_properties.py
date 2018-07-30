from programytest.storage.asserts.store.assert_properties import PropertyStoreAsserts

from programy.storage.stores.sql.store.properties import SQLPropertyStore
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.config import SQLStorageConfiguration


class SQLPropertyStoreTests(PropertyStoreAsserts):

    def test_initialise(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLPropertyStore(engine)
        self.assertEquals(store.storage_engine, engine)

    def test_properties_storage(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLPropertyStore(engine)

        self.assert_properties_storage(store)

    def test_property_storage(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLPropertyStore(engine)

        self.assert_property_storage(store)

    def test_empty_properties(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLPropertyStore(engine)

        self.assert_empty_properties(store)


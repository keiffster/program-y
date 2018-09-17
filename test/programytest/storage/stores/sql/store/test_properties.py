import unittest

from programytest.storage.asserts.store.assert_properties import PropertyStoreAsserts

from programy.storage.stores.sql.store.properties import SQLPropertyStore
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.config import SQLStorageConfiguration

import programytest.storage.engines as Engines


class SQLPropertyStoreTests(PropertyStoreAsserts):

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_initialise(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLPropertyStore(engine)
        self.assertEqual(store.storage_engine, engine)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_properties_storage(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLPropertyStore(engine)

        self.assert_properties_storage(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_property_storage(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLPropertyStore(engine)

        self.assert_property_storage(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_empty_properties(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLPropertyStore(engine)

        self.assert_empty_properties(store)


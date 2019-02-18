import unittest

from programytest.storage.asserts.store.assert_defaults import DefaultStoreAsserts

from programy.storage.stores.sql.store.properties import SQLDefaultVariableStore
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.config import SQLStorageConfiguration

import programytest.storage.engines as Engines


class SQLDefaultVariableStoreTests(DefaultStoreAsserts):

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_initialise(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLDefaultVariableStore(engine)
        self.assertEqual(store.storage_engine, engine)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_defaults_storage(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLDefaultVariableStore(engine)

        self.assert_defaults_storage(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_property_storage(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLDefaultVariableStore(engine)

        self.assert_defaults_storage(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_empty_defaults(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLDefaultVariableStore(engine)

        self.assert_empty_defaults(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_upload_from_file(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLDefaultVariableStore(engine)

        self.assert_upload_from_file(store)

import unittest

from programytest.storage.asserts.store.assert_variables import VariablesStoreAsserts


from programy.storage.stores.sql.store.variables import SQLVariablesStore
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.config import SQLStorageConfiguration

import programytest.storage.engines as Engines


class SQLVariablesStoreTests(VariablesStoreAsserts):

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_initialise(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLVariablesStore(engine)
        self.assertEqual(store.storage_engine, engine)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_variables_storage(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLVariablesStore(engine)

        self.assert_variables_storage(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_variable_storage(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLVariablesStore(engine)

        self.assert_variable_storage(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_empty_variables(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLVariablesStore(engine)

        self.assert_empty_variables(store)


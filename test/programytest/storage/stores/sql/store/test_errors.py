import unittest

from programytest.storage.asserts.store.assert_errors import ErrorStoreAsserts

from programy.storage.stores.sql.store.errors import SQLErrorsStore
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.config import SQLStorageConfiguration

import programytest.storage.engines as Engines


class SQLErrorsStoreTests(ErrorStoreAsserts):

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_initialise(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLErrorsStore(engine)
        self.assertEqual(store.storage_engine, engine)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_save_errors(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLErrorsStore(engine)

        self.assert_errors(store)


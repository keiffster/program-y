import unittest

from programytest.storage.asserts.store.assert_duplicates import DuplicateStoreAsserts

from programy.storage.stores.sql.store.duplicates import SQLDuplicatesStore
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.config import SQLStorageConfiguration

import programytest.storage.engines as Engines


class SQLDuplicatesStoreTests(DuplicateStoreAsserts):

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_initialise(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLDuplicatesStore(engine)
        self.assertEqual(store.storage_engine, engine)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_save_duplicates(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLDuplicatesStore(engine)

        self.assert_duplicates(store)

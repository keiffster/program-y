import unittest

from programytest.storage.asserts.store.assert_person2s import Person2sStoreAsserts

from programy.storage.stores.sql.store.lookups import SQLPerson2Store
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.config import SQLStorageConfiguration

import programytest.storage.engines as Engines


class SQLPerson2StoreTests(Person2sStoreAsserts):

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_initialise(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLPerson2Store(engine)
        self.assertEqual(store.storage_engine, engine)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_load_from_sql(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLPerson2Store(engine)

        self.assert_upload_from_file(store)

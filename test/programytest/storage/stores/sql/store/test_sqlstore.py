import unittest

import unittest.mock

from programy.storage.stores.sql.store.sqlstore import SQLStore
from programy.storage.stores.sql.engine import SQLStorageEngine

import programytest.storage.engines as Engines


class SQLStoreTests(unittest.TestCase):

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_initialise(self):

        config = unittest.mock.Mock()
        engine = SQLStorageEngine(config)
        store = SQLStore(engine)

        self.assertEqual(store.storage_engine, engine)

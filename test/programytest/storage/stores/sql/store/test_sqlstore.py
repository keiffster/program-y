import unittest
import unittest.mock

import programytest.storage.engines as Engines
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.store.sqlstore import SQLStore


class SQLStoreTests(unittest.TestCase):

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_initialise(self):

        config = unittest.mock.Mock()
        engine = SQLStorageEngine(config)
        store = SQLStore(engine)

        self.assertEqual(store.storage_engine, engine)

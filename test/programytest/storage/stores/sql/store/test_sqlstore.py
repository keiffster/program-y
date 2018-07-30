import unittest.mock

from programy.storage.stores.sql.store.sqlstore import SQLStore
from programy.storage.stores.sql.engine import SQLStorageEngine


class SQLStoreTests(unittest.TestCase):

    def test_initialise(self):

        config = unittest.mock.Mock()
        engine = SQLStorageEngine(config)
        store = SQLStore(engine)

        self.assertEquals(store.storage_engine, engine)

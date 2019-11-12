import unittest

import programytest.storage.engines as Engines
from programy.storage.engine import StorageEngineException
from programy.storage.stores.sql.config import SQLStorageConfiguration
from programy.storage.stores.sql.engine import SQLStorageEngine


class SQLBinariesStoreTests(unittest.TestCase):

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_initialise(self):

        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        with self.assertRaises(StorageEngineException):
            engine.binaries_store()


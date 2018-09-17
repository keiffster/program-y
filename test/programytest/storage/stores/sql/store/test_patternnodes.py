import unittest

from programytest.storage.asserts.store.assert_patternnodes import PatternNodesStoreAsserts

from programy.storage.stores.sql.store.nodes import SQLPatternNodesStore
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.config import SQLStorageConfiguration

import programytest.storage.engines as Engines


class SQLPatternNodesStoreTests(PatternNodesStoreAsserts):

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_initialise(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLPatternNodesStore(engine)
        self.assertEqual(store.storage_engine, engine)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_load_variables(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLPatternNodesStore(engine)

        self.assert_upload_from_file(store)


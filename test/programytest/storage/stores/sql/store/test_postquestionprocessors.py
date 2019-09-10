import unittest

from programytest.storage.asserts.store.assert_postquestionprocessors import PostQuestionProcessorsStoreAsserts

from programy.storage.stores.sql.store.processors import SQLPostQuestionProcessorsStore
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.config import SQLStorageConfiguration

import programytest.storage.engines as Engines


class SQLPostQuestionProcessorsStoreTests(PostQuestionProcessorsStoreAsserts):

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_initialise(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLPostQuestionProcessorsStore(engine)
        self.assertEqual(store.storage_engine, engine)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_upload_from_file(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLPostQuestionProcessorsStore(engine)

        self.assert_upload_from_file(store)


import unittest
import unittest.mock

import programytest.storage.engines as Engines
from programy.storage.stores.nosql.mongo.engine import MongoStorageEngine
from programy.storage.stores.nosql.mongo.store.mongostore import MongoStore


class MongoStoreTests(unittest.TestCase):

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_initialise(self):

        config = unittest.mock.Mock()
        engine = MongoStorageEngine(config)
        store = MongoStore(engine)

        self.assertEqual(store.storage_engine, engine)

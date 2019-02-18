import unittest
import unittest.mock

from programy.storage.stores.nosql.mongo.store.mongostore import MongoStore
from programy.storage.stores.nosql.mongo.engine import MongoStorageEngine

import programytest.storage.engines as Engines


class MongoStoreTests(unittest.TestCase):

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_initialise(self):

        config = unittest.mock.Mock()
        engine = MongoStorageEngine(config)
        store = MongoStore(engine)

        self.assertEqual(store.storage_engine, engine)

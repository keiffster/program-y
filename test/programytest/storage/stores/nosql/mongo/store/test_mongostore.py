import unittest.mock

from programy.storage.stores.nosql.mongo.store.mongostore import MongoStore
from programy.storage.stores.nosql.mongo.engine import MongoStorageEngine


class MongoStoreTests(unittest.TestCase):

    def test_initialise(self):

        config = unittest.mock.Mock()
        engine = MongoStorageEngine(config)
        store = MongoStore(engine)

        self.assertEquals(store.storage_engine, engine)

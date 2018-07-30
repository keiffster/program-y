from programytest.storage.asserts.store.assert_users import UserStoreAsserts

from programy.storage.stores.nosql.mongo.store.users import MongoUserStore
from programy.storage.stores.nosql.mongo.engine import MongoStorageEngine
from programy.storage.stores.nosql.mongo.config import MongoStorageConfiguration


class MongoUserStoreTests(UserStoreAsserts):

    def test_initialise(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoUserStore(engine)
        self.assertEquals(store.storage_engine, engine)

    def test_user_storage(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoUserStore(engine)

        self.assert_user_storage(store)

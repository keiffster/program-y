from programytest.storage.asserts.store.assert_linkedaccount import LinkedAccountStoreAsserts

from programy.storage.stores.nosql.mongo.store.linkedaccounts import MongoLinkedAccountStore
from programy.storage.stores.nosql.mongo.engine import MongoStorageEngine
from programy.storage.stores.nosql.mongo.config import MongoStorageConfiguration


class MongoLinkedAccountStoreTests(LinkedAccountStoreAsserts):

    def test_initialise(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoLinkedAccountStore(engine)
        self.assertEquals(store.storage_engine, engine)

    def test_linkedaccounts_storage(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoLinkedAccountStore(engine)

        self.assert_linkedaccounts_storage(store)
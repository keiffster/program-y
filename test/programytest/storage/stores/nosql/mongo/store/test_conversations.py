from programytest.storage.asserts.store.assert_conversations import ConverstionStoreAsserts

from programy.storage.stores.nosql.mongo.store.conversations import MongoConversationStore
from programy.storage.stores.nosql.mongo.engine import MongoStorageEngine
from programy.storage.stores.nosql.mongo.config import MongoStorageConfiguration


class MongoConversationStoreTests(ConverstionStoreAsserts):

    def test_initialise(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoConversationStore(engine)
        self.assertEquals(store.storage_engine, engine)

    def tests_conversation_storage(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoConversationStore(engine)
        self.assertEquals(store.storage_engine, engine)

        self.assert_conversation_storage(store)

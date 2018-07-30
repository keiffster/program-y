from programytest.storage.asserts.store.assert_conversations import ConverstionStoreAsserts

from programy.storage.stores.sql.store.conversations import SQLConversationStore
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.config import SQLStorageConfiguration


class SQLConversationStoreTests(ConverstionStoreAsserts):

    def test_initialise(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLConversationStore(engine)
        self.assertEquals(store.storage_engine, engine)

    def tests_conversation_storage(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLConversationStore(engine)
        self.assertEquals(store.storage_engine, engine)

        self.assert_conversation_storage(store)
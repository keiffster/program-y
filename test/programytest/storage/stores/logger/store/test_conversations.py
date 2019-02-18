from programytest.storage.asserts.store.assert_conversations import ConverstionStoreAsserts

from programy.storage.stores.logger.store.conversations import LoggerConversationStore
from programy.storage.stores.logger.engine import LoggerStorageEngine
from programy.storage.stores.logger.config import LoggerStorageConfiguration


class LoggerConversationStoreTests(ConverstionStoreAsserts):

    def test_initialise(self):
        config = LoggerStorageConfiguration()
        engine = LoggerStorageEngine(config)
        engine.initialise()
        store = LoggerConversationStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def tests_conversation_storage(self):
        config = LoggerStorageConfiguration()
        engine = LoggerStorageEngine(config)
        engine.initialise()
        store = LoggerConversationStore(engine)
        self.assertEqual(store.storage_engine, engine)

        self.assert_conversation_storage(store, can_empty=False, test_load=False)
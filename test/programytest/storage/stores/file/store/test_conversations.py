from programytest.storage.asserts.store.assert_conversations import ConverstionStoreAsserts

from programy.storage.stores.file.store.conversations import FileConversationStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration


class FileConversationStoreTests(ConverstionStoreAsserts):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileConversationStore(engine)
        self.assertEquals(store.storage_engine, engine)

    def tests_conversation_storage(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileConversationStore(engine)
        self.assertEquals(store.storage_engine, engine)

        self.assert_conversation_storage(store, can_empty=True, test_load=True)
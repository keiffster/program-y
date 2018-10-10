from programytest.storage.asserts.store.assert_conversations import ConverstionStoreAsserts

from programy.storage.stores.file.store.conversations import FileConversationStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration
import os.path
import shutil

class FileConversationStoreTests(ConverstionStoreAsserts):

    def setUp(self):
        self._tmpdir = os.path.dirname(__file__) + os.sep + "conversations"

    def tearDown(self):
        if os.path.exists(self._tmpdir):
            shutil.rmtree(self._tmpdir)
        self.assertFalse(os.path.exists(self._tmpdir))

    def test_initialise(self):
        config = FileStorageConfiguration()
        config.conversation_storage._dirs = [self._tmpdir]

        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileConversationStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def tests_conversation_storage(self):
        config = FileStorageConfiguration()
        config.conversation_storage._dirs = [self._tmpdir]

        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileConversationStore(engine)
        self.assertEqual(store.storage_engine, engine)

        self.assert_conversation_storage(store, can_empty=True, test_load=True)


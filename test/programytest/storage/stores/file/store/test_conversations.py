import os.path
import shutil
from unittest.mock import patch
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.store.conversations import FileConversationStore
from programytest.storage.asserts.store.assert_conversations import ConverstionStoreAsserts
from programy.storage.stores.file.store.config import FileStoreConfiguration
from programytest.client import TestClient
from programy.dialog.conversation import Conversation
from programy.dialog.question import Question


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

    def test_storage_path(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileConversationStore(engine)

        self.assertEquals('/tmp/conversations', store._get_storage_path())
        self.assertIsInstance(store.get_storage(), FileStoreConfiguration)

    def test_conversation_storage(self):
        config = FileStorageConfiguration()
        config.conversation_storage._dirs = [self._tmpdir]

        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileConversationStore(engine)
        self.assertEqual(store.storage_engine, engine)

        self.assert_conversation_storage(store, can_empty=True, test_load=True)

    def patch_write_file(self, conversation_filepath, json_text):
        raise Exception("Mock Exception")

    @patch('programy.storage.stores.file.store.conversations.FileConversationStore._write_file', patch_write_file)
    def test_save_conversation_with_exception(self):
        config = FileStorageConfiguration()
        config.conversation_storage._dirs = [self._tmpdir]

        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileConversationStore(engine)

        store.empty()

        client = TestClient()
        client_context = client.create_client_context("user1")

        conversation = Conversation(client_context)

        question1 = Question.create_from_text(client_context, "Hello There")
        question1.sentence(0).response = "Hi"
        conversation.record_dialog(question1)

        store.store_conversation(client_context, conversation)

    def patch_read_file(self, conversation_filepath, conversation):
        raise Exception("Mock Exception")

    @patch('programy.storage.stores.file.store.conversations.FileConversationStore._read_file', patch_read_file)
    def test_load_conversation_with_exception(self):
        config = FileStorageConfiguration()
        config.conversation_storage._dirs = [self._tmpdir]

        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileConversationStore(engine)

        store.empty()

        client = TestClient()
        client_context = client.create_client_context("user1")

        conversation = Conversation(client_context)

        question1 = Question.create_from_text(client_context, "Hello There")
        question1.sentence(0).response = "Hi"
        conversation.record_dialog(question1)

        store.store_conversation(client_context, conversation)

        conversation = Conversation(client_context)
        store.load_conversation(client_context, conversation)

from programy.storage.stores.logger.config import LoggerStorageConfiguration
from programy.storage.stores.logger.engine import LoggerStorageEngine
from programy.storage.stores.logger.store.conversations import LoggerConversationStore
from programytest.storage.asserts.store.assert_conversations import ConverstionStoreAsserts
from programy.dialog.conversation import Conversation
from programy.dialog.question import Question
from programytest.client import TestClient


class MockLoggerConversationStore(LoggerConversationStore):

    def __init__(self, storage_engine):
        LoggerConversationStore.__init__(self, storage_engine)
        self.logged = False

    def _get_logger(self):
        return None

    def _log_conversation(self, convo_logger, client_context, conversation):
        self.logged = True


class LoggerConversationStoreTests(ConverstionStoreAsserts):

    def test_initialise(self):
        config = LoggerStorageConfiguration()
        engine = LoggerStorageEngine(config)
        engine.initialise()
        store = LoggerConversationStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_conversation_storage(self):
        config = LoggerStorageConfiguration()
        engine = LoggerStorageEngine(config)
        engine.initialise()
        store = LoggerConversationStore(engine)
        self.assertEqual(store.storage_engine, engine)

        self.assert_conversation_storage(store, can_empty=False, test_load=False)

    def test_store_conversation(self):
        config = LoggerStorageConfiguration()
        engine = LoggerStorageEngine(config)
        engine.initialise()
        store = LoggerConversationStore(engine)

        client = TestClient()
        client_context = client.create_client_context("user1")

        conversation = Conversation(client_context)

        question1 = Question.create_from_text(client_context, "Hello There")
        question1.sentence(0).response = "Hi"
        conversation.record_dialog(question1)

        store.store_conversation(client_context, conversation)

    def test_store_converstion_no_logger(self):
        config = LoggerStorageConfiguration()
        store = MockLoggerConversationStore(config)

        client = TestClient()
        client_context = client.create_client_context("user1")

        conversation = Conversation(client_context)

        question1 = Question.create_from_text(client_context, "Hello There")
        question1.sentence(0).response = "Hi"
        conversation.record_dialog(question1)

        store.store_conversation(client_context, conversation)

        self.assertFalse(store.logged)

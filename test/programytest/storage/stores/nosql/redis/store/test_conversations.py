import unittest

import programytest.storage.engines as Engines
from programy.dialog.conversation import Conversation
from programy.dialog.question import Question
from programy.storage.stores.nosql.redis.config import RedisStorageConfiguration
from programy.storage.stores.nosql.redis.engine import RedisStorageEngine
from programy.storage.stores.nosql.redis.store.conversations import RedisConversationStore
from programytest.client import TestClient


class MockRedisConversationStore(RedisConversationStore):

    def __init__(self, storage_engine, fail_write=False, fail_read=False):
        RedisConversationStore.__init__(self, storage_engine)
        self._fail_write = fail_write
        self._fail_read = fail_read

    def _write_conversation(self, client_context, conversation):
        if self._fail_write is True:
            raise Exception("Mock exception")
        super(MockRedisConversationStore)._write_conversation(client_context, conversation)

    def _read_conversation(self, client_context, conversation):
        if self._fail_read is True:
            raise Exception("Mock exception")
        super(MockRedisConversationStore)._read_conversation(client_context, conversation)


class RedisConversationStoreTests(unittest.TestCase):

    @unittest.skipIf(Engines.redis is False, Engines.redis_disabled)
    def test_initialise(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        engine.initialise()
        store = RedisConversationStore(engine)
        self.assertEqual(store.storage_engine, engine)

    @unittest.skipIf(Engines.redis is False, Engines.redis_disabled)
    def test_conversations_storage(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        engine.initialise()
        store = RedisConversationStore(engine)

        client = TestClient()
        client_context = client.create_client_context("user1")

        conversation1 = Conversation(client_context)

        conversation1.properties['ckey1'] = "cvalue1"
        conversation1.properties['ckey2'] ="cvalue2"

        question1 = Question.create_from_text(client_context, "Hello There")
        question1.sentence(0).response = "Hi"
        question1.sentence(0)._positivity = 0.5
        question1.sentence(0)._subjectivity = 0.6
        question1.properties['qkey1'] = "qvalue1"
        question1.properties['qkey2'] = "qvalue2"

        conversation1.record_dialog(question1)

        store.store_conversation(client_context, conversation1)

        conversation2 = Conversation(client_context)

        store.load_conversation(client_context, conversation2)
        self.assertIsNotNone(conversation2)

        self.assertEqual(conversation2.properties['ckey1'], "cvalue1")
        self.assertEqual(conversation2.properties['ckey2'], "cvalue2")

        self.assertEqual(conversation2.questions[0].sentence(0).response, "Hi")
        self.assertEqual(conversation2.questions[0].sentence(0)._positivity, 0.5)
        self.assertEqual(conversation2.questions[0].sentence(0)._subjectivity, 0.6)

        self.assertEqual(conversation2.questions[0].properties['qkey1'], "qvalue1")
        self.assertEqual(conversation2.questions[0].properties['qkey2'], "qvalue2")

        store.empty()

    @unittest.skipIf(Engines.redis is False, Engines.redis_disabled)
    def test_conversations_storage_exception_on_save_load(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        engine.initialise()
        store = MockRedisConversationStore(engine, fail_write=False, fail_read=False)

        client = TestClient()
        client_context = client.create_client_context("user1")

        conversation1 = Conversation(client_context)

        store.store_conversation(client_context, conversation1)

        conversation2 = Conversation(client_context)

        store.load_conversation(client_context, conversation2)

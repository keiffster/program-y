import unittest

from programy.storage.stores.nosql.redis.store.conversations import RedisConversationStore
from programy.storage.stores.nosql.redis.engine import RedisStorageEngine
from programy.storage.stores.nosql.redis.config import RedisStorageConfiguration
from programy.dialog.conversation import Conversation
from programy.dialog.question import Question

import programytest.storage.engines as Engines

from programytest.client import TestClient


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

        self.assertEquals(conversation2.properties['ckey1'], "cvalue1")
        self.assertEquals(conversation2.properties['ckey2'], "cvalue2")

        self.assertEquals(conversation2.questions[0].sentence(0).response, "Hi")
        self.assertEquals(conversation2.questions[0].sentence(0)._positivity, 0.5)
        self.assertEquals(conversation2.questions[0].sentence(0)._subjectivity, 0.6)

        self.assertEquals(conversation2.questions[0].properties['qkey1'], "qvalue1")
        self.assertEquals(conversation2.questions[0].properties['qkey2'], "qvalue2")

        store.empty()

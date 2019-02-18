import unittest

from programy.config.bot.redisstorage import BotConversationsRedisStorageConfiguration
from programy.dialog.storage.redis import ConversationRedisStorage
from programytest.client import TestClient
from programy.dialog.dialog import Conversation


class ConversationRedisStorageTests(unittest.TestCase):

    def test_persistence(self):

        storage_config = BotConversationsRedisStorageConfiguration("redis")
        redis = ConversationRedisStorage(storage_config)
        self.assertIsNotNone(redis)

        client = TestClient()
        client_context = client.create_client_context("testid")
        conversation1 = Conversation(client_context)
        conversation1.set_property("topic", "topic1")

        redis.save_conversation(conversation1, client_context.userid)

        conversation2 = Conversation(client_context)
        redis.load_conversation(conversation2, client_context.userid)
        self.assertIsNotNone(conversation2)
        self.assertIsNotNone(conversation2.properties)

        self.assertEqual(conversation1.properties, conversation2.properties)


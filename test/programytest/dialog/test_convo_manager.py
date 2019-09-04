import unittest
import shutil
import os

from programy.config.bot.conversations import BotConversationsConfiguration
from programy.dialog.convo_mgr import ConversationManager
from programy.dialog.question import Question

from programytest.client import TestClient


class ConversationManagerTests(unittest.TestCase):

    def test_init(self):
        config = BotConversationsConfiguration()
        mgr = ConversationManager(config)

        self.assertEqual(mgr.configuration, config)
        self.assertIsNone(mgr.storage)
        self.assertEqual(mgr.conversations, {})

    def test_initialise(self):
        config = BotConversationsConfiguration()
        mgr = ConversationManager(config)

        client = TestClient()
        client.add_conversation_store("./storage/conversations")

        mgr.initialise(client.storage_factory)
        self.assertIsNotNone(mgr.storage)

    def test_conversation_operations(self):
        config = BotConversationsConfiguration()
        mgr = ConversationManager(config)

        if os.path.exists("./storage/conversations"):
            shutil.rmtree("./storage/conversations")

        client = TestClient()
        client.add_conversation_store("./storage/conversations")

        mgr.initialise(client.storage_factory)

        client_context = client.create_client_context("user1")

        conversation = mgr.get_conversation(client_context)

        question1 = Question.create_from_text(client_context, "Hello There")
        question1.sentence(0).response = "Hi"
        conversation.record_dialog(question1)
        mgr.save_conversation(client_context)

        question2 = Question.create_from_text(client_context, "Hello There Again")
        question2.sentence(0).response = "Hi Again"
        conversation.record_dialog(question2)
        mgr.save_conversation(client_context)

        question3 = Question.create_from_text(client_context, "Hello There Again Again")
        question3.sentence(0).response = "Hi Again Again"
        conversation.record_dialog(question3)
        mgr.save_conversation(client_context)

        self.assertEqual(len(mgr.conversations), 1)
        mgr.empty()
        self.assertEqual(len(mgr.conversations), 0)

        conversation = mgr.get_conversation(client_context)
        self.assertEqual(len(mgr.conversations), 1)

        if os.path.exists("./storage/conversations"):
            shutil.rmtree("./storage/conversations")

        self.assertIsNotNone(conversation)
        self.assertEqual(len(conversation.questions), 3)


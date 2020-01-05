import os
import shutil
import unittest

from programy.config.bot.conversations import BotConversationsConfiguration
from programy.dialog.convo_mgr import ConversationManager
from programy.dialog.question import Question
from programy.storage.factory import StorageFactory
from programytest.client import TestClient


class MockStorageFactory(StorageFactory):

    def __init__(self):
        StorageFactory.__init__(self)

    def entity_storage_engine_available(self, name):
        return True

    def entity_storage_engine(self, name):
        return None


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

    def test_initialise_storage_engine_failed(self):
        config = BotConversationsConfiguration()
        mgr = ConversationManager(config)

        mgr.initialise(MockStorageFactory())
        self.assertIsNone(mgr.storage)

    def get_temp_dir(self):
        if os.name == 'posix':
            return '/tmp'
        elif os.name == 'nt':
            import tempfile
            return tempfile.gettempdir()
        else:
            raise Exception("Unknown operating system [%s]" % os.name)

    def test_conversation_operations(self):
        config = BotConversationsConfiguration()
        config._multi_client = False
        mgr = ConversationManager(config)

        convo_dir = self.get_temp_dir() + os.sep + "storage" + os.sep + "conversations"

        if os.path.exists(convo_dir):
            shutil.rmtree(convo_dir)

        client = TestClient()
        client.add_conversation_store(convo_dir)

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

        if os.path.exists(convo_dir):
            shutil.rmtree(convo_dir)

        self.assertIsNotNone(conversation)
        self.assertEqual(len(conversation.questions), 3)

    def test_conversation_operations_multi_client(self):
        config = BotConversationsConfiguration()
        config._multi_client = True
        mgr = ConversationManager(config)

        convo_dir = self.get_temp_dir() + os.sep + "storage" + os.sep + "conversations"

        if os.path.exists(convo_dir):
            shutil.rmtree(convo_dir)

        client = TestClient()
        client.add_conversation_store(convo_dir)

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

        conversation2 = mgr.get_conversation(client_context)
        self.assertIsNotNone(conversation2)

        self.assertEqual(len(mgr.conversations), 1)
        mgr.empty()
        self.assertEqual(len(mgr.conversations), 0)

        conversation = mgr.get_conversation(client_context)
        self.assertEqual(len(mgr.conversations), 1)

        if os.path.exists(convo_dir):
            shutil.rmtree(convo_dir)

        self.assertIsNotNone(conversation)
        self.assertEqual(len(conversation.questions), 3)

    def test_conversation_operations_multi_client_no_storage(self):
        config = BotConversationsConfiguration()
        config._multi_client = True
        mgr = ConversationManager(config)

        convo_dir = self.get_temp_dir() + os.sep + "storage" + os.sep + "conversations"

        if os.path.exists(convo_dir):
            shutil.rmtree(convo_dir)

        client = TestClient()
        #client.add_conversation_store(convo_dir)

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

        conversation2 = mgr.get_conversation(client_context)
        self.assertIsNotNone(conversation2)

        self.assertEqual(len(mgr.conversations), 1)
        mgr.empty()
        self.assertEqual(len(mgr.conversations), 0)

        conversation = mgr.get_conversation(client_context)
        self.assertEqual(len(mgr.conversations), 1)

        if os.path.exists(convo_dir):
            shutil.rmtree(convo_dir)

        self.assertIsNotNone(conversation)
        self.assertEqual(len(conversation.questions), 0)

    def test_conversation_operations_wrong_userid(self):
        config = BotConversationsConfiguration()
        mgr = ConversationManager(config)

        convo_dir = self.get_temp_dir() + os.sep + "storage" + os.sep + "conversations"

        if os.path.exists(convo_dir):
            shutil.rmtree(convo_dir)

        client = TestClient()
        client.add_conversation_store(convo_dir)

        mgr.initialise(client.storage_factory)

        client_context = client.create_client_context("user1")

        conversation = mgr.get_conversation(client_context)

        question1 = Question.create_from_text(client_context, "Hello There")
        question1.sentence(0).response = "Hi"
        conversation.record_dialog(question1)
        mgr.save_conversation(client_context)

        client_context2 = client.create_client_context("user2")
        mgr.save_conversation(client_context2)

    def test_conversation_operations_no_conversation(self):
        config = BotConversationsConfiguration()
        mgr = ConversationManager(config)

        convo_dir = self.get_temp_dir() + os.sep + "storage" + os.sep + "conversations"

        if os.path.exists(convo_dir):
            shutil.rmtree(convo_dir)

        client = TestClient()
        client.add_conversation_store(convo_dir)

        mgr.initialise(client.storage_factory)

        client_context = client.create_client_context("user1")

        conversation = mgr.get_conversation(client_context)

        question1 = Question.create_from_text(client_context, "Hello There")
        question1.sentence(0).response = "Hi"
        conversation.record_dialog(question1)

        del mgr._conversations[client_context.userid]

        mgr.save_conversation(client_context)

    def test_conversation_operations_no_default_variables(self):
        config = BotConversationsConfiguration()
        config._multi_client = False
        mgr = ConversationManager(config)

        convo_dir = self.get_temp_dir() + os.sep + "storage" + os.sep + "conversations"

        if os.path.exists(convo_dir):
            shutil.rmtree(convo_dir)

        client = TestClient()
        client.add_conversation_store(convo_dir)

        mgr.initialise(client.storage_factory)

        client_context = client.create_client_context("user1")
        client_context.brain._default_variables_collection = None

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

        if os.path.exists(convo_dir):
            shutil.rmtree(convo_dir)

        self.assertIsNotNone(conversation)
        self.assertEqual(len(conversation.questions), 3)


import unittest
import os

from programy.dialog.dialog import Sentence, Question, Conversation
from programy.bot import Bot
from programy.brain import Brain
from programy.config.brain.brain import BrainConfiguration
from programy.config.bot.bot import BotConfiguration
from programy.config.bot.filestorage import BotConversationsFileStorageConfiguration
from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient

class ConversationFileStorageTests(unittest.TestCase):

    def test_persistence(self):
        client = TestClient()
        client_context = client.create_client_context("testid")
        bot_config = BotConfiguration()
        bot_config.conversations._type = "file"
        bot_config.conversations._storage = BotConversationsFileStorageConfiguration("test")
        bot_config.conversations._storage._dir = os.path.dirname(__file__)
        bot_config.conversations._max_histories = 3
        client_context.bot = Bot(bot_config)

        filename = bot_config.conversations._storage._dir + os.sep + client_context.userid + ".convo"
        if os.path.exists(filename):
            os.remove(filename)
        self.assertFalse(os.path.exists(filename))

        conversation = client_context.bot.get_conversation(client_context)
        conversation.properties['name'] = "fred"

        client_context.bot.save_conversation(client_context.userid)
        self.assertTrue(os.path.exists(filename))

        test_bot2 = Bot(bot_config)
        conversation2 = test_bot2.get_conversation(client_context)
        self.assertIsNotNone(conversation2.property('name'))
        self.assertEqual('fred', conversation2.property('name'))

        self.assertTrue(os.path.exists(filename))
        if os.path.exists(filename):
            os.remove(filename)
        self.assertFalse(os.path.exists(filename))

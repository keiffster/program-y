import unittest
import os

from programy.dialog.dialog import Sentence, Question, Conversation
from programy.bot import Bot
from programy.brain import Brain
from programy.config.sections.brain.brain import BrainConfiguration
from programy.config.sections.bot.bot import BotConfiguration
from programy.config.sections.bot.filestorage import BotConversationsFileStorageConfiguration

class ConversationPersistenceTests(unittest.TestCase):

    def test_persistence(self):
        brain_config = BrainConfiguration()
        test_brain = Brain(brain_config)
        bot_config = BotConfiguration()
        bot_config.conversations._type = "file"
        bot_config.conversations._storage = BotConversationsFileStorageConfiguration("test")
        bot_config.conversations._storage._dir = os.path.dirname(__file__)
        bot_config.conversations._max_histories = 3
        test_bot = Bot(test_brain, bot_config)

        clientid = "test"

        filename = bot_config.conversations._storage._dir + os.sep + clientid + ".convo"
        if os.path.exists(filename):
            os.remove(filename)
        self.assertFalse(os.path.exists(filename))

        conversation = test_bot.get_conversation(clientid)
        conversation.properties['name'] = "fred"

        test_bot.save_conversation(clientid)
        self.assertTrue(os.path.exists(filename))

        test_bot2 = Bot(test_brain, bot_config)
        conversation2 = test_bot2.get_conversation(clientid)
        self.assertIsNotNone(conversation2.property('name'))
        self.assertEqual('fred', conversation2.property('name'))

        self.assertTrue(os.path.exists(filename))
        if os.path.exists(filename):
            os.remove(filename)
        self.assertFalse(os.path.exists(filename))

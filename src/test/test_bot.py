import unittest

from programy.brain import Brain
from programy.bot import Bot
from programy.config.client.client import ClientConfiguration
from programy.config.brain import BrainConfiguration
from programy.config.bot import BotConfiguration

class BotTests(unittest.TestCase):

    def test_bot_init_default_brain(self):
        test_brain = Brain(BrainConfiguration())
        bot = Bot(test_brain, BotConfiguration())
        self.assertIsNotNone(bot)
        self.assertIsNotNone(bot.brain)

    def test_bot_init_supplied_brain(self):
        test_brain = Brain(BrainConfiguration())
        bot = Bot(test_brain, BotConfiguration())
        self.assertIsNotNone(bot)
        self.assertIsNotNone(bot.brain)

    def test_bot_defaultresponses(self):
        test_brain = Brain(BrainConfiguration())
        bot = Bot(test_brain, BotConfiguration())
        self.assertIsNotNone(bot)
        self.assertEqual(bot.prompt, ">>> ")
        self.assertEqual(bot.default_response, "Sorry, I don't have an answer for that right now")
        self.assertEqual(bot.exit_response, "Bye!")

    def test_bot_with_config(self):
        configuration = ClientConfiguration()
        self.assertIsNotNone(configuration)
        self.assertIsNotNone(configuration.bot_configuration)
        self.assertIsNotNone(configuration.brain_configuration)

        configuration.bot_configuration.prompt = ":"
        configuration.bot_configuration.default_response = "No answer for that"
        configuration.bot_configuration.exit_response = "See ya!"

        test_brain = Brain(BrainConfiguration())
        test_brain.load(configuration.brain_configuration)

        bot = Bot(test_brain, config=configuration.bot_configuration)
        self.assertIsNotNone(bot)

        self.assertEqual(bot.prompt, ":")
        self.assertEqual(bot.default_response, "No answer for that")
        self.assertEqual(bot.exit_response, "See ya!")

    def test_bot_with_conversation(self):
        test_brain = Brain(BrainConfiguration())
        self.assertIsNotNone(test_brain)

        bot = Bot(test_brain, BotConfiguration())
        self.assertIsNotNone(bot)

        self.assertFalse(bot.has_conversation("testid"))

        response = bot.ask_question("testid", "hello")
        self.assertIsNotNone(response)
        self.assertTrue(bot.has_conversation("testid"))

        response = bot.ask_question("testid", "hello")
        self.assertIsNotNone(response)
        self.assertTrue(bot.has_conversation("testid"))

        response = bot.ask_question("testid2", "hello")
        self.assertIsNotNone(response)
        self.assertTrue(bot.has_conversation("testid2"))

    def test_bot_chat_loop(self):
        test_brain = Brain(BrainConfiguration())
        self.assertIsNotNone(test_brain)
        self.assertIsInstance(test_brain, Brain)

        bot = Bot(test_brain, BotConfiguration())
        self.assertIsNotNone(bot)
        self.assertIsInstance(bot, Bot)

        response = bot.ask_question("testid", "hello")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Sorry, I don't have an answer for that right now")

        response = bot.ask_question("testid", "hello again")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Sorry, I don't have an answer for that right now")

        response = bot.ask_question("testid", "goodbye")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Sorry, I don't have an answer for that right now")

        conversation = bot.get_conversation("testid")
        self.assertIsNotNone(conversation)

        self.assertEqual(conversation.nth_question(3).sentence(0).text(), "hello")
        self.assertEqual(conversation.nth_question(3).sentence(0).response, "Sorry, I don't have an answer for that right now")

        self.assertEqual(conversation.nth_question(2).sentence(0).text(), "hello again")
        self.assertEqual(conversation.nth_question(2).sentence(0).response, "Sorry, I don't have an answer for that right now")

        self.assertEqual(conversation.nth_question(1).sentence(0).text(), "goodbye")
        self.assertEqual(conversation.nth_question(1).sentence(0).response, "Sorry, I don't have an answer for that right now")

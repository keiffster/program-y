import unittest

from programy.bot import Bot
from programy.bot import BrainFactory
from programy.brain import Brain
from programy.config.bot.bot import BotConfiguration
from programytest.client import TestClient


class BrainFactoryTests(unittest.TestCase):

    def test_init(self):

        client = TestClient()

        bot = Bot(BotConfiguration(), client)

        self.assertIsNotNone(bot.brain_factory)
        self.assertIsInstance(bot.brain_factory, BrainFactory)

        brain = bot.brain_factory.brain("brain")

        self.assertIsNotNone(brain)

    def test_empty_config_init(self):
        configuration = BotConfiguration()

        client = TestClient()
        bot = Bot(configuration, client)

        factory = BrainFactory(bot)
        self.assertIsNotNone(factory)

        brain = factory.select_brain()
        self.assertIsNotNone(brain)
        self.assertIsInstance(brain, Brain)

    def test_config_init(self):
        configuration = BotConfiguration()
        configuration._brain_selector = "programy.clients.client.DefaultBrainSelector"

        client = TestClient()
        bot = Bot(configuration, client)

        factory = BrainFactory(bot)
        self.assertIsNotNone(factory)

        brain = factory.select_brain()
        self.assertIsNotNone(brain)
        self.assertIsInstance(brain, Brain)

    def test_invalid_config_init(self):
        configuration = BotConfiguration()
        configuration._brain_selector = "programy.clients.client.DefaultBrainSelectorXXX"

        client = TestClient()
        bot = Bot(configuration, client)

        factory = BrainFactory(bot)
        self.assertIsNotNone(factory)

        brain = factory.select_brain()
        self.assertIsNotNone(brain)
        self.assertIsInstance(brain, Brain)

